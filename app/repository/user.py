from sqlalchemy.orm import Session 
from app.db import models
from fastapi import HTTPException,status 
from app.hashing import Hash

def crear_usuario(usuario,db:Session):
    usuario = usuario.dict()
    try:
        nuevo_usuario = models.User(
            username=usuario["username"],
            password=Hash.hash_password(usuario["password"]),
            nombre=usuario["nombre"],
            apellido=usuario["apellido"],
            direccion=usuario["direccion"],
            telefono=usuario["telefono"],
            correo=usuario["correo"],
        )
        db.add(nuevo_usuario)
        db.commit()
        db.refresh(nuevo_usuario)
    except Exception as e :
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Error creando usuario {e}"
        )

def obtener_usuario(user_id,db:Session):
    usuario = db.query(models.User).filter(models.User.id == user_id ).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe el usuario con el id {user_id}"
        )
    return usuario

def eliminar_usuario(user_id,db:Session):
    usuario = db.query(models.User).filter(models.User.id == user_id )
    if not usuario.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe el usuario con el id {user_id} por lo tanto no se elimina"
        )
    usuario.delete(synchronize_session=False)
    db.commit()
    return {"respuesta":"Usuario eliminado correctamente!"}

def obtener_usuarios(db:Session):
    data = db.query(models.User).all()
    return data

def actualizar_user(user_id,updateUser,db:Session):
    usuario = db.query(models.User).filter(models.User.id == user_id )
    if not usuario.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe el usuario con el id {user_id}"
        )
    usuario.update(updateUser.dict( exclude_unset=True))
    db.commit()
    return {"respuesta":"Usuario actualizado correctamente!"}