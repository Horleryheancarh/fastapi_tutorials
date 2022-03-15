from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import schemas, database, models, token
from ..hashing import Hash


router = APIRouter(
	tags=['Authentication']
)


@router.post('/login')
def login(request: schemas.Login, db: Session = Depends(database.get_db)):
	user = db.query(models.User).filter(models.User.email == request.username).first()

	if not user:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")


	if Hash.verify(user.password, request.password):
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Password")
	

	# generate JWT token and return it
	access_token = token.create_access_token(data={"sub": user.email})

	return {"access_token": access_token, "token_type": "bearer"}