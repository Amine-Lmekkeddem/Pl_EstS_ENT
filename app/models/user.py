from pydantic import BaseModel, EmailStr, validator
import datetime
from typing import Optional
from uuid import UUID  # Assuming you have a UUID class defined somewhere

class user(BaseModel):
    id: UUID  # Primary key from Keycloak
    username : str
    email : EmailStr
    role : str
    student_number : str 
    department : str  
    profile_picture: Optional[str] = None 
    status : str = "active" 
    created_at : datetime.datetime  # Timestamp for when the user was created


@validator('student_number')
def convert_student_number(cls, v):
    return str(v)  # Convert to string for storage

class CreateUserRequest(BaseModel):
    username: str
    email: str
    role: str
    student_number: str
    department: str
    profile_picture: str = ""
    status: str = "inactive"
    temporary_password: Optional[str] = None
