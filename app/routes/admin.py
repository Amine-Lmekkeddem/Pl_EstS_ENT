from fastapi import APIRouter, Depends, HTTPException, status
from app.models.user import CreateUserRequest, user
from app.services.keycloak_admin import create_user_in_keycloak
#from app.db.cassandra_connector import get_cassandra_session
from uuid import uuid4
from datetime import datetime
from app.auth.jwt import verify_token
from fastapi.security import OAuth2PasswordBearer
from uuid import uuid4
from datetime import datetime
import secrets
import string
import logging
from traceback import format_exc
from app.db.cassandra_connector import connect_to_cassandra
from uuid import UUID
from cassandra.cluster import Cluster
from app.config import settings
from app.services.keycloak_admin import delete_user_from_keycloak
from app.services.User_service import UserService
from app.dependencies import get_user_service
router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login", auto_error=True)

def generate_temp_password(length=12):
    """Generate a random temporary password"""
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(chars) for _ in range(length))

user_service = UserService()

@router.post("/users", status_code=201)
async def create_user(
    user_request: CreateUserRequest,
    token: str = Depends(oauth2_scheme),
    user_service: UserService = Depends(get_user_service)
):
    try:
        # Auth check remains the same
        token = await verify_token(token)
        if "admin" not in token["roles"]:
            raise HTTPException(status_code=403, detail="Admin privileges required")

        return await user_service.create_user(user_request)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))