from typing import Optional
from datetime import timedelta
from jose import JWTError, jwt


SECRET_KEY='6ea36dcbec271856595d8c89c893eed9b2d1d2e546001b4b4e0cdec221289bd9'
ALGORITHM='HS256'
ACCESS_TOKEN_EXPIRE_MINUTES=60


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
	
	to_encode = data.copy()

	expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
	
	to_encode.update({"exp": expire})
	encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

	return encoded_jwt
