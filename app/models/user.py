from pydantic import BaseModel, EmailStr
import datetime
from typing import Optional

class user(BaseModel):
    username : str
    email : EmailStr
    role : str
    student_number : int 
    department : str  
    profile_picture: Optional[str] = None 
    status : str = "active" 
    created_at : datetime.datetime  # Timestamp for when the user was created

class CreateUserRequest(BaseModel):
    username: str
    email: str
    role: str
    student_number: int
    department: str
    profile_picture: str = ""
    status: str = "inactive"
    temporary_password: Optional[str] = None
