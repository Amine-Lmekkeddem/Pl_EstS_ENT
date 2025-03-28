#upload.py
from fastapi import APIRouter, File, UploadFile, HTTPException, Form, Depends
from app.services.services import process_file_upload


router = APIRouter()

@router.post("/uploadfile/")
async def upload_file(
    course_id: str = Form(...),  # UUID du cours
    uploaded_by: str = Form(...),  # UUID de l'utilisateur
    file: UploadFile = File(...),  # Fichier à télécharger
):
    """
    Route pour télécharger un fichier et enregistrer les informations associées.
    """
    try:
        # Appeler la fonction `process_file_upload` pour traiter l'upload du fichier
        result = process_file_upload(course_id, uploaded_by, file)
        return result
    except HTTPException as e:
        raise e




