from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from database.connection import get_db

from auth.schemas.models import (
    RoleDelete,
    RoleCreate,
    RoleUpdate,
    Permission,
)

from auth.utils.role_crud import (
    role_create,
    role_get_all,
    role_delete,
    role_get_one,
    role_update,
    role_add_a_permission,
    role_remove_a_permission,
)

router = APIRouter(tags=["Roles"])


@router.post("/create" , status_code=status.HTTP_201_CREATED) # response_model=UserCreate
def create_role(
    record : RoleCreate,
    db: Session = Depends(get_db),
):
  
    return role_create(db=db , record=record)

@router.get("/list/all" , status_code=status.HTTP_200_OK , ) 
def get_all_roles(
    db: Session = Depends(get_db),
):
    return role_get_all(db=db)

@router.get("/get/{id}", status_code=status.HTTP_200_OK, ) 
def get_one_role(id, db: Session = Depends(get_db)):
    return role_get_one(db=db, id=id)

@router.put("/update" , status_code=status.HTTP_200_OK , ) 
def update_role(
    record : RoleUpdate,
    db: Session = Depends(get_db),    
):
    return role_update(db=db , record=record)

@router.put("/update/add-a-permission/{role_id}" , status_code=status.HTTP_200_OK, )
def add_permission_to_role(
    role_id : UUID,
    permission : Permission,
    db : Session = Depends(get_db),
):

    return role_add_a_permission(db=db , role_id=role_id , permission=permission)

@router.put("/update/remove-a-permission/{role_id}" , status_code=status.HTTP_200_OK, )
def remove_permission_to_role(
    role_id : UUID,
    permission : Permission,
    db : Session = Depends(get_db),
):

    return role_remove_a_permission(db=db , role_id=role_id , permission=permission)

@router.delete(
    "/delete/{id}" , 
    status_code=status.HTTP_200_OK , 
    response_model=RoleDelete
)
def delete_role(
    id,
    db : Session = Depends(get_db),
):
    return role_delete(db=db , id=id)

