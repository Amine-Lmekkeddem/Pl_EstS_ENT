import httpx
from app.config import settings
from app.models.token import Token

async def get_token(username: str, password: str) -> Token:
    token_url = f"{settings.KEYCLOAK_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/token"
    data = {
        "client_id": settings.KEYCLOAK_CLIENT_ID,
        "client_secret": settings.KEYCLOAK_CLIENT_SECRET,
        "grant_type": "password",
        "username": username,
        "password": password,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, data=data)

        if response.status_code != 200:
            raise Exception("Invalid credentials or Keycloak error")

        token_data = response.json()
        return Token(access_token=token_data["access_token"], token_type=token_data["token_type"])
