from pydantic import BaseModel,EmailStr
from typing import Optional

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass

    
class UserOut(BaseModel):
    id:int
    email:EmailStr
    class Config:
          from_attributes=True

class Post(BaseModel):
      title:str
      content:str
      published:bool
      owner_id:int
      owner:UserOut
      class Config:
          from_attributes=True
          
class UserCreate(BaseModel):
    email:EmailStr
    password:str
          
        
class UserLogin(BaseModel):
    email:EmailStr
    password:str
    
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None