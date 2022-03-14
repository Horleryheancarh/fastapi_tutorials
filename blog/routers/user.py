from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from .. import database, schemas, models
from ..hashing import Hash


router = APIRouter()

@router.post('/user', response_model=schemas.ShowUser, tags=['user'])
def create_user(request: schemas.User, db: Session = Depends(database.get_db)):

	new_user = models.User(name=request.name, email=request.email, password=Hash.bcrypt(request.password))
	db.add(new_user)
	db.commit()
	db.refresh(new_user)

	return new_user


@router.get('/user/{id}', response_model=schemas.ShowUser, tags=['user'])
def get_user(id: int, db: Session = Depends(database.get_db)):
	user = db.query(models.User).filter(models.User.id == id).first()

	if not user:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with the id {id} is not available")
	
	return user


@router.get('/user', tags=['user'])
def all_users(db: Session = Depends(database.get_db)):
	users = db.query(models.User).all()

	return users


@router.put('/user/{id}', tags=['user'])
def update_user(id: int, request: schemas.User, db: Session = Depends(database.get_db)):
	user = db.query(models.User).filter(models.User.id == id)

	if not user.first():
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with the id {id} is not available")
	
	user.update(request)
	db.commit()

	return {'updated'}

