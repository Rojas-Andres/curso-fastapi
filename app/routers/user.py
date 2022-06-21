from fastapi import APIRouter,Depends,status 
from app.schemas import User,ShowUser,UpdateUser
from app.db.database import get_db
from sqlalchemy.orm import Session 
from typing import List
from app.repository import user 
from app.oauth import get_current_user
router = APIRouter(
    prefix="/user",
    tags=["Users"]
)

@router.get('/',response_model=List[ShowUser],status_code=status.HTTP_200_OK)
def obtener_usuarios(db:Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    data = user.obtener_usuarios(db)
    return data

@router.post('/',status_code=status.HTTP_201_CREATED)
def crear_usuario(usuario:User,db:Session = Depends(get_db)):
    user.crear_usuario(usuario,db)
    return {"respuesta":"Usuario creado satisfactoriamente!!"}

@router.get('/{user_id}',response_model=ShowUser,status_code=status.HTTP_200_OK)
def obtener_usuario(user_id:int,db:Session = Depends(get_db)):
    usuario = user.obtener_usuario(user_id,db)
    return usuario

@router.delete('/{user_id}',status_code=status.HTTP_200_OK)
def eliminar_usuario(user_id:int,db:Session = Depends(get_db)):
    res = user.eliminar_usuario(user_id, db)
    return res 

@router.patch('/{user_id}',status_code=status.HTTP_200_OK)
def actualizar_user(user_id:int,updateUser:UpdateUser,db:Session = Depends(get_db)):
    res = user.actualizar_user(user_id,updateUser, db)
    return res 