from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserModel(BaseModel):
    name:str
    email:EmailStr
    password:str
    city:str
    role:Optional[str] = None
    phone:Optional[str] = None
    created_at:Optional[str] = Field(default_factory=lambda: datetime.now().isoformat())