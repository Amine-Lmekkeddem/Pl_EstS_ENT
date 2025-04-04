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

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login", auto_error=True)

def generate_temp_password(length=12):
    """Generate a random temporary password"""
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(chars) for _ in range(length))

@router.post("/users", status_code=201)
async def create_user(
    user_data: CreateUserRequest,
    # session=Depends(get_cassandra_session),
    token: str = Depends(oauth2_scheme)
):
    #print(token)
    try:
        # Verify the token and extract user information
        token = await verify_token(token)
        # if not token:
        #     raise HTTPException(status_code=401, detail="Not authenticated")
        # 👇 Check if current user has 'admin' role
        if "admin" not in token["roles"]:
            raise HTTPException(status_code=403, detail="Admin privileges required")

        temp_password = generate_temp_password()  # Generate or define logic
        result = await create_user_in_keycloak(
            username=user_data.username,
            email=user_data.email,
            role=user_data.role,
            temp_password=temp_password
        )

        print(f"Keycloak result: {result}")
        created_at = datetime.utcnow()

        query = """
        INSERT INTO users (
            username, email, role, student_number,
            department, profile_picture, status, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        # session.execute(
        #     query,
        #     (
        #         user_data.username,
        #         user_data.email,
        #         user_data.role,
        #         user_data.student_number,
        #         user_data.department,
        #         user_data.profile_picture,
        #         user_data.status,
        #         created_at,
        #     )
        # )

        return {
            "message": "User successfully created",
            "keycloak_user_id": result["user_id"],
            "temporary_password": temp_password
        }

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"error {str(e)}")
    
    