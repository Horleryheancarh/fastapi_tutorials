from pydantic import BaseModel
from typing import List, Optional


class BlogBase(BaseModel):
	title: str
	body: str


# Request Schema
class User(BaseModel):
	name: str
	email: str
	password: str


class Blog(BlogBase):
	class Config():
		orm_mode = True


# Response Schema
class ShowUser(User):
	name: str
	email: str
	blogs: List[Blog] = []

	class Config():
		orm_mode = True


class ShowBlog(Blog):
	title: str
	body: str
	creator: ShowUser

	class Config():
		orm_mode = True


class Login(BaseModel):
	username: str
	password: str


class Token(BaseModel):
	access_token: str
	token_type: str


class TokenData(BaseModel):
	username: Optional[str] = None


