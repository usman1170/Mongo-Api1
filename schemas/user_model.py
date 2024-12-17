from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional

class UserModel(BaseModel):
    name:str
    email:EmailStr
    password:str
    role:Optional[str] = None
    phone:Optional[str] = None
    created_at:Optional[str] = datetime.now()