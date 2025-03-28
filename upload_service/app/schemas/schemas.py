from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

# Schéma Pydantic pour le téléchargement de fichiers (validation)
class UploadFileRequest(BaseModel):
    course_id: str
    uploaded_by: str
    file: str  # Nom du fichier
