from fastapi.testclient import TestClient
import sys 
import os 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
from main import app 
from app.db.models import Base 
from app.hashing import Hash
from app.db.database import get_db
import time 
db_path = os.path.join(os.path.dirname(__file__),'test.db')
db_uri = "sqlite:///{}".format(db_path)
SQLALCHEMY_DATABASE_URL = db_uri
engine_test = create_engine(SQLALCHEMY_DATABASE_URL,connect_args={"check_same_thread":False })
TestingSessionLocal = sessionmaker(bind=engine_test,autocommit=False,autoflush=False)
Base.metadata.create_all(bind=engine_test)

cliente = TestClient(app)
def insertar_usuario_prueba():

    password_hash = Hash.hash_password('prueba12')

    engine_test.execute(
        f"""
        INSERT INTO usuario(username,password,nombre,apellido,direccion,telefono,correo)
        values
        ('prueba','{password_hash}','prueba_nombre','prueba_apellido','prueba_direccion',1212,'prueba@gmail.com')
        """
    )
insertar_usuario_prueba()


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

def test_crear_usuario():
    usuario = {
        "username": "andres1",
        "password": "1",
        "nombre": "string",
        "apellido": "string",
        "direccion": "string",
        "telefono": 0,
        "correo": "an@gmail.com",
        "creacion_user": "2022-06-11T00:07:49.786586"    
    }
    response = cliente.post('/user/',json=usuario)
    assert response.status_code == 401

    usuario_login = {
        "username":"prueba",
        "password":"prueba12"
    }

    response_token = cliente.post('/login/',data=usuario_login)
    assert response_token.status_code == 200
    assert response_token.json()["token_type"] == "bearer"

    headers = {
        "Authorization":f"Bearer {response_token.json()['access_token']}"
    }
    response = cliente.post('/user/',json=usuario,headers=headers)
    assert response.status_code == 201
    assert response.json()["respuesta"] == "Usuario creado satisfactoriamente!!"

def test_obtener_usuarios():
    usuario_login = {
        "username":"prueba",
        "password":"prueba12"
    }
    response_token = cliente.post('/login/',data=usuario_login)
    assert response_token.status_code == 200
    assert response_token.json()["token_type"] == "bearer"

    headers = {
        "Authorization":f"Bearer {response_token.json()['access_token']}"
    }
    response = cliente.get('/user/',headers=headers)
    assert len(response.json()) == 2

def test_obtener_usuario():
    response = cliente.get('/user/1')
    assert response.json()["username"] == "prueba"

def test_eliminar_usuario():
    response = cliente.delete('/user/1')
    assert response.json()["respuesta"] == "Usuario eliminado correctamente!"
    response_user = cliente.get('/user/1')
    assert response_user.json()["detail"] == "No existe el usuario con el id 1"

def test_actualizar_usuario():
    usuario = {
        "username": "andres1_actualizado",
    }
    response = cliente.patch('/user/2',json=usuario)
    assert response.json()["respuesta"] == 'Usuario actualizado correctamente!'

    response_user = cliente.get('/user/2')
    assert response_user.json()["username"] == "andres1_actualizado"
    assert response_user.json()["nombre"] == "string"

def test_no_encuentra_usuario():
    usuario = {
        "username": "andres1_actualizado",
    }
    response = cliente.patch('/user/12',json=usuario)
    assert response.json()["detail"] == 'No existe el usuario con el id 12'

def test_delete_database():
    db_path = os.path.join(os.path.dirname(__file__),'test.db')
    os.remove(db_path)