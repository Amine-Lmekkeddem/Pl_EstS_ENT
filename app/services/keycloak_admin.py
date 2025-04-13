import httpx
from fastapi import HTTPException
from app.config import settings  # adjust to your actual path

async def get_admin_token():
    """
    Obtains an admin token from Keycloak using the admin-cli client
    """
    try:
        keycloak_url = "http://localhost:8080"  # Replace with your Keycloak URL
        realm = "master"  # Typically 'master' for admin operations
        client_id = "admin-cli"  # Default admin client
        username = "admin"  # Your Keycloak admin username
        password = "KEYcloak024"  # Your Keycloak admin password
        
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


async def delete_user_from_keycloak(user_id: str):
    """
    Delete a user from Keycloak using the same authentication pattern as create_user_in_keycloak
    Args:
        user_id: Keycloak user ID (UUID string)
    Returns:
        dict: Status message
    Raises:
        HTTPException: If any step in the deletion process fails
    """
    try:
        # Get admin token using the same method as create_user_in_keycloak
        access_token = await get_admin_token()
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        # Construct the delete URL
        delete_url = f"{settings.KEYCLOAK_URL}/admin/realms/{settings.KEYCLOAK_REALM}/users/{user_id}"
        
        async with httpx.AsyncClient() as client:
            # First verify the user exists
            get_user_url = f"{settings.KEYCLOAK_URL}/admin/realms/{settings.KEYCLOAK_REALM}/users/{user_id}"
            user_response = await client.get(get_user_url, headers=headers)
            
            if user_response.status_code == 404:
                return {"status": "success", "message": "User not found, nothing to delete"}
            
            if user_response.status_code != 200:
                raise HTTPException(
                    status_code=user_response.status_code,
                    detail=f"Failed to verify user: {user_response.text}"
                )
            
            # Delete the user
            delete_response = await client.delete(delete_url, headers=headers)
            
            if delete_response.status_code not in [200, 204]:
                raise HTTPException(
                    status_code=delete_response.status_code,
                    detail=f"Failed to delete user: {delete_response.text}"
                )
            
            return {"status": "success", "message": "User deleted successfully"}
    
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Keycloak API error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete user from Keycloak: {str(e)}"
        )