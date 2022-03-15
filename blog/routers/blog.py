from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, database, models
from ..controllers import blog


router = APIRouter(
	prefix="/blog",
	tags=['blogs']
	)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowBlog)
def create(request: schemas.Blog, db: Session = Depends(database.get_db)):
	return blog.create(request, db)


@router.get('/', response_model=List[schemas.ShowBlog])
def get_all(db: Session = Depends(database.get_db)):
	return blog.get_all(db)


@router.get('/{id}', response_model=schemas.ShowBlog)
def single(id: int, db: Session = Depends(database.get_db)):
	return blog.get(id, db)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.Blog, db: Session =Depends((database.get_db))):
	return blog.update(id, request, db)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(database.get_db)):
	return blog.destroy(id, db)
