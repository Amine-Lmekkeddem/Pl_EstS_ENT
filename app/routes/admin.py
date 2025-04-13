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
from app.services.cassandra_service import CassandraService
from app.models.Course import course, CreateCourseRequest
from app.services.cources_serivce import CourseService
router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login", auto_error=True)

# def generate_temp_password(length=12):
#     """Generate a random temporary password"""
#     chars = string.ascii_letters + string.digits + "!@#$%^&*"
#     return ''.join(secrets.choice(chars) for _ in range(length))

user_service = UserService()
# and point to add user to cassandra and keycloak
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
# end point to delete user from cassandra and keycloak
@router.delete("/users/{user_id}")
async def delete_user(
    user_id: UUID,
    token: str = Depends(oauth2_scheme)
):
    """
    Delete user from both systems
    Requires admin privileges
    """
    try:
        # Verify admin privileges
        token = await verify_token(token)
        if "admin" not in token["roles"]:
            raise HTTPException(status_code=403, detail="Admin privileges required")

        result = await user_service.delete_user(user_id)
        
        if not result["success"]:
            status_code = 500
            if "Keycloak" in result["message"]:
                status_code = 502  # Bad Gateway
            raise HTTPException(status_code=status_code, detail=result["message"])

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    
course_service = CourseService()
# end point to add courses to cassandra 
@router.post("/courses", status_code=201)
async def create_course(
    course_data: CreateCourseRequest,
    token: str = Depends(oauth2_scheme),
):
    try:
        # Auth check remains the same
        token = await verify_token(token)
        if "admin" not in token["roles"]:
            raise HTTPException(status_code=403, detail="Admin privileges required")

        return await course_service.create_course(course_data)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# end to delete cources from cassandra
@router.delete("/courses/{course_id}")
async def delete_course(
    course_id: UUID,
    token: str = Depends(oauth2_scheme)  # Add your auth dependency
):
    """
    Delete a course by ID
    - Requires admin or teacher privileges
    """
    try:
         # Auth check remains the same
        token = await verify_token(token)
        if "admin" not in token["roles"]:
            raise HTTPException(status_code=403, detail="Admin privileges required")

        
        result = await course_service.delete_course(course_id)
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["message"])
            
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))