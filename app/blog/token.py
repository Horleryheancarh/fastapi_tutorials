import os
from typing import Optional
from datetime import timedelta, datetime
from jose import JWTError, jwt
from dotenv import load_dotenv, find_dotenv

from blog import schemas

load_dotenv(find_dotenv())

secret = os.getenv('SECRET_KEY')
alg = os.getenv('ALGORITHM')
exp = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
	
	to_encode = data.copy()

	expire = datetime.utcnow() + timedelta(minutes=exp)
	
	to_encode.update({"exp": expire})
	encoded_jwt = jwt.encode(to_encode, secret, algorithm=alg)

	return encoded_jwt


def verify_token(token: str, credentials_exception):
	try:
		payload = jwt.decode(token, secret, algorithms=[alg])
		email: str = payload.get("sub")
		if email is None:
			raise credentials_exception
		
		token_data = schemas.TokenData(email=email)
	except JWTError:
		raise credentials_exception