from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from database.connection import get_db

from auth.models import User
from auth.schemas.models import UserCreate , UserDelete , UserUpdate , UserCheck

from auth.utils.user_crud import (
    user_create,
    user_delete,
    user_get_all,
    user_get_one,
    user_update,
    user_assign_to_group,
    user_get_metadata,
    user_update_metadata,
)


router = APIRouter(tags=["Users"])


@router.post("/create" , status_code=status.HTTP_201_CREATED) # response_model=UserCreate
def create_user(
    record : UserCreate,
    db: Session = Depends(get_db),
):
  
    return user_create(db=db , record=record)

@router.get("/list/all" , status_code=status.HTTP_200_OK , ) # response_model=List[UserCreate]
def get_all_users(
    db: Session = Depends(get_db),
):
    return user_get_all(db=db)

@router.get("/get/{id}", status_code=status.HTTP_200_OK, ) # response_model=UserCreate
def get_one_user(id, db: Session = Depends(get_db)):
    return user_get_one(db=db, id=id)

@router.get("/get/metadata/{id}" , status_code=status.HTTP_200_OK)
def get_user_metadata(id , db : Session = Depends(get_db)):
    return user_get_metadata(id=id , db=db) 

@router.put("/update/metadata/{id}" , status_code=status.HTTP_200_OK)
def update_user_metadata(id , metadata : dict , db : Session = Depends(get_db)):
    return user_update_metadata(id=id , db=db , metadata=metadata)

@router.put("/update" , status_code=status.HTTP_200_OK , ) # response_model=UserCreate
def update_user(
    record : UserUpdate,
    db: Session = Depends(get_db),    
):
    return user_update(db=db , record=record)

@router.delete(
    "/delete/{id}" , 
    status_code=status.HTTP_200_OK , 
    response_model=UserDelete
)
def delete_user(
    id,
    db : Session = Depends(get_db),
):
    return user_delete(db=db , id=id)

@router.post(
    "/assign-to-group/{user_id}/{group_id}",
    status_code=status.HTTP_201_CREATED,
)
def assign_user_to_group(
    user_id : UUID,
    group_id : UUID,
    db : Session = Depends(get_db),
):

    return user_assign_to_group(db=db , user_id=user_id , group_id=group_id)



        
    