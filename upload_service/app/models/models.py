from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

# Modèle Pydantic pour la validation des données
class FileMetadata(BaseModel):
    file_id: UUID
    course_id: str
    file_name: str
    file_url: str
    file_type: str
    file_size: int
    uploaded_by: str
    uploaded_at: datetime
