import httpx
from fastapi import HTTPException
from app.config import settings  # adjust to your actual path

# async def get_admin_token():
#     token_url = f"{settings.KEYCLOAK_URL}/realms/master/protocol/openid-connect/token"
#     data = {
#         #"client_id": "admin-cli",
#         "client_id": settings.KEYCLOAK_CLIENT_ID,
#         "grant_type": "client_credentials",
#         "client_secret": settings.KEYCLOAK_CLIENT_SECRET,
#         # "username": settings.KEYCLOAK_ADMIN_USER,
#         # "password": settings.KEYCLOAK_ADMIN_PASSWORD,
#     }

#     async with httpx.AsyncClient() as client:
#         response = await client.post(token_url, data=data)

#     if response.status_code != 200:
#         raise HTTPException(status_code=500, detail="Failed to authenticate with Keycloak")

#     return response.json()["access_token"]

async def get_admin_token():
    """
    Obtains an admin token from Keycloak using the admin-cli client
    """
    try:
        keycloak_url = "http://localhost:8080"  # Replace with your Keycloak URL
        realm = "master"  # Typically 'master' for admin operations
        client_id = "admin-cli"  # Default admin client
        username = "admin"  # Your Keycloak admin username
        password = "admin"  # Your Keycloak admin password
        
        token_url = f"{keycloak_url}/realms/{realm}/protocol/openid-connect/token"
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                token_url,
                data={
                    "client_id": client_id,
                    "username": username,
                    "password": password,
                    "grant_type": "password"
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Keycloak error: {response.text}"
                )
            
            return response.json()["access_token"]
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get admin token: {str(e)}"
        )
async def create_user_in_keycloak(username: str, email: str, role: str, temp_password: str):
    access_token = await get_admin_token()

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # 1. Create the user
    create_user_url = f"{settings.KEYCLOAK_URL}/admin/realms/{settings.KEYCLOAK_REALM}/users"
    user_payload = {
        "username": username,
        "email": email,
        "enabled": True,
    }

    async with httpx.AsyncClient() as client:
        create_response = await client.post(create_user_url, json=user_payload, headers=headers)

        if create_response.status_code not in [201, 204]:
            raise HTTPException(status_code=500, detail=f"Failed to create user: {create_response.text}")

        # 2. Get the user ID from location header
        location = create_response.headers.get("Location")
        user_id = location.split("/")[-1] if location else None
        if not user_id:
            raise HTTPException(status_code=500, detail="User ID not found after creation")

        # 3. Set temporary password
        reset_password_url = f"{create_user_url}/{user_id}/reset-password"
        password_payload = {
            "type": "password",
            "value": temp_password,
            "temporary": True
        }

        await client.put(reset_password_url, json=password_payload, headers=headers)

        # 4. Assign Role (Realm role)
        role_url = f"{create_user_url}/{user_id}/role-mappings/realm"
        role_representation_url = f"{settings.KEYCLOAK_URL}/admin/realms/{settings.KEYCLOAK_REALM}/roles/{role}"

        role_response = await client.get(role_representation_url, headers=headers)
        if role_response.status_code != 200:
            raise HTTPException(status_code=404, detail=f"Role '{role}' not found")

        role_data = role_response.json()
        await client.post(role_url, json=[role_data], headers=headers)

    return {"message": "User created and configured in Keycloak", "user_id": user_id}
