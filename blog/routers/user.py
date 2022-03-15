from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from .. import database, schemas, models
from ..hashing import Hash
from ..controllers import user


router = APIRouter(
	prefix="/user",
	tags=['user']
	)

@router.post('/', response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(database.get_db)):
	return user.create(request, db)


@router.get('/{id}', response_model=schemas.ShowUser)
def get_user(id: int, db: Session = Depends(database.get_db)):
	return user.get(id, db)


@router.get('/')
def all_users(db: Session = Depends(database.get_db)):
	return user.get_all(db)


@router.put('/{id}')
def update_user(id: int, request: schemas.User, db: Session = Depends(database.get_db)):
	return user.update(id, request, db)

