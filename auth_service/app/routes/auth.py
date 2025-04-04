from fastapi import APIRouter, HTTPException
from app.schemas.auth_schema import LoginRequest
from app.services.auth_service import get_token
from app.models.token import Token
from fastapi import Depends
from app.utils.keycloak import verify_token, check_user_role, oauth2_scheme

router = APIRouter()

# @router.post("/login", response_model=Token)
# async def login(login_request: LoginRequest):
#     try:
#         token = await get_token(login_request.username, login_request.password)
#         return token
#     except Exception as e:
#         raise HTTPException(status_code=401, detail=str(e))
# auth_service - route login
@router.post("/login", response_model=Token)
async def login(login_request: LoginRequest):
    try:
        token = await get_token(login_request.username, login_request.password)
        return token  # Le token est généré ici
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

# admin route
@router.get("/admin", dependencies=[Depends(verify_token)])
async def admin_route(token: str = Depends(oauth2_scheme)):
    # Check if user has the admin role
    await check_user_role(token, ["admin"])
    return {"message": "Welcome, Admin!"}
# student route 
@router.get("/student", dependencies=[Depends(verify_token)])
async def student_route(token: str = Depends(oauth2_scheme)):
    # Check if user has the student role
    await check_user_role(token, ["student"])
    return {"message": "Welcome, Student!"}
# teacher route
@router.get("/teacher", dependencies=[Depends(verify_token)])
async def teacher_route(token: str = Depends(oauth2_scheme)):
    # Check if user has the teacher role
    await check_user_role(token, ["Teacher"])
    return {"message": "Welcome, Teacher!"}

@router.get("/protected", dependencies=[Depends(verify_token)])
async def protected_route():
    return {"message": "You have access to this protected route!"}