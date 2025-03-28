# service.py
import uuid
from datetime import datetime
from app.config import get_cassandra_connection, get_minio_client
from fastapi import HTTPException, UploadFile

# Configuration de la connexion à Cassandra et MinIO
cassandra_session = get_cassandra_connection()
minio_client = get_minio_client()

# Fonction pour enregistrer le fichier dans MinIO
def upload_to_minio(file: UploadFile, file_id: uuid.UUID):
    file_location = f"files/{file_id}/{file.filename}"
    file.file.seek(0)  # Réinitialiser le pointeur du fichier au début
    file_size = len(file.file.read())  # Lire le fichier pour obtenir la taille
    file.file.seek(0)  # Réinitialiser de nouveau le pointeur du fichier pour l'upload

    try:
        minio_client.put_object(
            bucket_name="course-files",  # Assurez-vous d'avoir créé un bucket dans MinIO
            object_name=file_location,
            data=file.file,
            length=file_size
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'upload vers MinIO: {e}")

    return file_location

# Fonction pour enregistrer les métadonnées dans Cassandra
def save_file_metadata(file_id: uuid.UUID, course_id: uuid.UUID, file: UploadFile, file_url: str, uploaded_by: uuid.UUID):
    uploaded_at = datetime.now()
    try:
        session = cassandra_session
        session.execute("""
        INSERT INTO files (file_id, course_id, file_name, file_url, file_type, file_size, uploaded_by, uploaded_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (file_id, course_id, file.filename, file_url, file.content_type, len(file.file.read()), uploaded_by, uploaded_at))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'enregistrement dans Cassandra: {e}")

# Fonction principale pour traiter l'upload du fichier
def process_file_upload(course_id: str, uploaded_by: str, file: UploadFile):
    # Convertir les paramètres de chaîne en UUID
    try:
        course_id = uuid.UUID(course_id)
        uploaded_by = uuid.UUID(uploaded_by)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format.")

    file_id = uuid.uuid4()

    # Upload du fichier dans MinIO
    file_url = upload_to_minio(file, file_id)

    # Enregistrer les métadonnées dans Cassandra
    save_file_metadata(file_id, course_id, file, file_url, uploaded_by)

    return {"file_id": file_id, "file_url": file_url, "message": "File uploaded successfully"}
