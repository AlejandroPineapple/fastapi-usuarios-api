from typing import List
from fastapi import HTTPException, APIRouter
from db.db import collection
from model.usuario import Usuario

router = APIRouter()
#hola xas
@router.post("/", response_description="Crear un nuevo Usuario", response_model= Usuario)
async def create_usuario(usuario: Usuario):

    existing_user = await collection.find_one({"email": usuario.email})

    if existing_user != None:
        raise HTTPException(status_code=404, detail="Email ya existe")
    result = await collection.insert_one(usuario.dict())
    usuario._id = str(result.inserted_id)
    return usuario

@router.get (path="/", response_description="Listar Usuarios", response_model= List[Usuario])
async def read_usuarios():
    usuarios = await collection.find().to_list(100)

    for usuario in usuarios:
        usuario["_id"] = str(usuario["_id"])
        print (usuario)

    return usuarios

@router.put(path="/{email}", response_model=Usuario)
async def update_usuario(email: str, usuario: Usuario):
    updated_usuario = await collection.find_one_and_update({"email": email}, {"$set": usuario.dict()})

    if updated_usuario:
        return usuario
    raise HTTPException(status_code=404, detail="Lo busco lo busco y no lo busco")

@router.delete(path="/{email}", response_model=Usuario)
async def delete_usuario(email: str):
    deleted_usuario = await collection.find_one_and_delete({"email": email})

    if deleted_usuario:
        return deleted_usuario
    raise HTTPException(status_code=404, detail="Lo busco lo busco y no lo busco")
