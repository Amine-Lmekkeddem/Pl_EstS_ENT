# #upload.py
# from fastapi import APIRouter, File, UploadFile, HTTPException, Form, Depends
# from app.services.services import process_file_upload
# from app.utils.keycloak import verify_token_with_auth_service
# from fastapi.security import OAuth2PasswordBearer

# # OAuth2PasswordBearer pour l'extraction du token depuis le header Authorization
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# router = APIRouter()

# @router.post("/uploadfile/")
# async def upload_file(
#     course_id: str = Form(...),  # UUID du cours
#     uploaded_by: str = Form(...),  # UUID de l'utilisateur
#     file: UploadFile = File(...),  # Fichier à télécharger
#     token: str = Depends(oauth2_scheme)  # Extraction du token via OAuth2PasswordBearer
# ):
#     """
#     Route pour télécharger un fichier et enregistrer les informations associées.
#     """
#     try:
#          # Valider le token avec auth_service
#         token_info = await verify_token_with_auth_service(token)
        
#         # Appeler la fonction `process_file_upload` pour traiter l'upload du fichier
#         result = process_file_upload(course_id, uploaded_by, file)
#         return result
#     except HTTPException as e:
#         raise HTTPException(status_code=e.status_code, detail=e.detail)

#     # Si la validation du token est réussie, procéder à l'upload
#     return {"message": "File uploaded successfully", "user_info": token_info}


# upload_service.py
from fastapi import APIRouter, File, UploadFile, HTTPException, Form, Depends
from app.services.services import process_file_upload
from app.utils.keycloak import verify_token_with_auth_service  # Importer la fonction de validation
from fastapi.security import OAuth2PasswordBearer

# OAuth2PasswordBearer pour l'extraction du token depuis le header Authorization
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

router = APIRouter()

@router.post("/uploadfile/")
async def upload_file(
    course_id: str = Form(...),  # UUID du cours
    file: UploadFile = File(...),  # Fichier à télécharger
    token: str = Depends(oauth2_scheme)  # Extraction du token via OAuth2PasswordBearer
):
    """
    Route pour télécharger un fichier et enregistrer les informations associées.
    """
    try:
        # Vérifier le token et obtenir les informations de l'utilisateur
        token_info = await verify_token_with_auth_service(token)
        uploaded_by = token_info["user_id"]  # Extraire l'user_id à partir des informations du token
        
        # Appeler la fonction `process_file_upload` pour traiter l'upload du fichier
        result = process_file_upload(course_id, uploaded_by, file)
        return result
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
        # Si la validation du token est réussie, procéder à l'upload
        return {"message": "File uploaded successfully", "user_info": token_info}