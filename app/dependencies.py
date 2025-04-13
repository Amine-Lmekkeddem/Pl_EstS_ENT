# app/dependencies.py
from app.services.User_service import UserService

def get_user_service():
    return UserService()