from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, database, models


router = APIRouter()


@router.post('/blog', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowBlog, tags=['blog'])
def create_blog(request: schemas.Blog, db: Session = Depends(database.get_db)):
	new_blog = models.Blog(title=request.title, body=request.body)
	db.add(new_blog)
	db.commit()
	db.refresh(new_blog)
	
	return new_blog


@router.get('/blog', response_model=List[schemas.ShowBlog], tags=['blog'])
def all_blogs(db: Session = Depends(database.get_db)):
	blogs = db.query(models.Blog).all()
	
	return blogs


@router.get('/blog/{id}', response_model=schemas.ShowBlog, tags=['blog'])
def single_blog(id: int, db: Session = Depends(database.get_db)):
	blog = db.query(models.Blog).filter(models.Blog.id == id).first()
	
	if not blog:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} is not available")

	return blog


@router.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['blog'])
def destroy_blog(id: int, db: Session = Depends(database.get_db)):
	blog = db.query(models.Blog).filter(models.Blog.id == id)
	
	if not blog.first():
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} is not available")
	
	blog.delete(synchronize_session=False)
	db.commit()
	
	return {'done'}


@router.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['blog'])
def update_blog(id: int, request: schemas.Blog, db: Session =Depends((database.get_db))):
	blog = db.query(models.Blog).filter(models.Blog.id == id)

	if not blog.first():
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} is not available")
	
	blog.update(request)
	db.commit()
	
	return {'updated'}