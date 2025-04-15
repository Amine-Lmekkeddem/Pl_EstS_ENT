import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
       # Keycloak Settings
    KEYCLOAK_URL = os.getenv("KEYCLOAK_URL")
    KEYCLOAK_REALM = os.getenv("KEYCLOAK_REALM")
    KEYCLOAK_CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID")
    KEYCLOAK_CLIENT_SECRET = os.getenv("KEYCLOAK_CLIENT_SECRET")
    KEYCLOAK_ADMIN_USER = os.getenv("KEYCLOAK_ADMIN_USER")
    KEYCLOAK_ADMIN_PASSWORD = os.getenv("KEYCLOAK_ADMIN_PASSWORD")

    # Cassandra Settings
    CASSANDRA_HOST = os.getenv("CASSANDRA_HOST")
    CASSANDRA_PORT = int(os.getenv("CASSANDRA_PORT", 9042))
    CASSANDRA_KEYSPACE = os.getenv("CASSANDRA_KEYSPACE")

    # Ollama Settings
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3:instruct")
    
    # Validate required variables
    if not all([
        KEYCLOAK_URL, KEYCLOAK_REALM, KEYCLOAK_CLIENT_ID, KEYCLOAK_CLIENT_SECRET
    ]):
        raise ValueError("Missing required Keycloak environment variables!")

settings = Settings()
 