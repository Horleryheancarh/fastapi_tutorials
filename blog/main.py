from fastapi import FastAPI, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from passlib.context import CryptContext

from . import schemas, models
from .database import engine, SessionLocal

app = FastAPI()


models.Base.metadata.create_all(engine)

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()


@app.post('/blog', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowBlog, tags=['blog'])
def create_blog(request: schemas.Blog, db: Session = Depends(get_db)):
	new_blog = models.Blog(title=request.title, body=request.body)
	db.add(new_blog)
	db.commit()
	db.refresh(new_blog)
	
	return new_blog


@app.get('/blog', response_model=List[schemas.ShowBlog], tags=['blog'])
def all_blogs(db: Session = Depends(get_db)):
	blogs = db.query(models.Blog).all()
	
	return blogs


@app.get('/blog/{id}', response_model=schemas.ShowBlog, tags=['blog'])
def single_blog(id: int, db: Session = Depends(get_db)):
	blog = db.query(models.Blog).filter(models.Blog.id == id).first()
	
	if not blog:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} is not available")

	return blog


@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['blog'])
def destroy_blog(id: int, db: Session = Depends(get_db)):
	blog = db.query(models.Blog).filter(models.Blog.id == id)
	
	if not blog.first():
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} is not available")
	
	blog.delete(synchronize_session=False)
	db.commit()
	
	return {'done'}


@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['blog'])
def update_blog(id: int, request: schemas.Blog, db: Session =Depends((get_db))):
	blog = db.query(models.Blog).filter(models.Blog.id == id)

	if not blog.first():
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} is not available")
	
	blog.update(request)
	db.commit()
	
	return {'updated'}


@app.post('/user', response_model=schemas.ShowUser, tags=['user'])
def create_user(request: schemas.User, db: Session = Depends(get_db)):
	hashed_password = pwd_cxt.hash(request.password)

	new_user = models.User(name=request.name, email=request.email, password=hashed_password)
	db.add(new_user)
	db.commit()
	db.refresh(new_user)

	return new_user


@app.get('/user/{id}', response_model=schemas.ShowUser, tags=['user'])
def get_user(id: int, db: Session = Depends(get_db)):
	user = db.query(models.User).filter(models.User.id == id).first()

	if not user:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with the id {id} is not available")
	
	return user


@app.get('/user', tags=['user'])
def all_users(db: Session = Depends(get_db)):
	users = db.query(models.User).all()

	return users


@app.put('/user/{id}', tags=['user'])
def update_user(id: int, request: schemas.User, db: Session = Depends(get_db)):
	user = db.query(models.User).filter(models.User.id == id)

	if not user.first():
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with the id {id} is not available")
	
	user.update(request)
	db.commit()

	return {'updated'}






