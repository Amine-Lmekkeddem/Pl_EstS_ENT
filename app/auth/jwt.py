import httpx
from fastapi import HTTPException, Security, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from jose.constants import ALGORITHMS
from app.config import settings
from jose.backends.rsa_backend import RSAKey
from fastapi import HTTPException
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



# OAuth2PasswordBearer for token extraction
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login", auto_error=True)

# Fetch Keycloak public keys from the JWKS endpoint
async def get_keycloak_public_key():
    url = f"{settings.KEYCLOAK_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/certs"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to fetch public keys")
        return response.json()

# Decode and validate the JWT
async def verify_token(token: str = Depends(oauth2_scheme)):
    if not token:
        logger.error("No token provided")
        raise HTTPException(status_code=401, detail="No token provided")
    try:
        # Extract header and get the kid (key id)
        unverified_header = jwt.get_unverified_header(token)
        kid = unverified_header.get("kid")
        #print(f"Kid: {kid}")
        # Get public keys from Keycloak
        keys = await get_keycloak_public_key()
        #print(f"Keys: {keys}")
        key = next((k for k in keys["keys"] if k["kid"] == kid), None)

        if not key:
            raise HTTPException(status_code=401, detail="Invalid token: Key not found")

        # Construct the RSA public key
        # public_key = jwt.algorithms.RSAAlgorithm.from_jwk(key)
        #public_key = jwt.construct(key)
        public_key = RSAKey(key, ALGORITHMS.RS256)
        #print(f"Public Key: {public_key}")

        # Decode and validate token
        payload = jwt.decode(token,
                            public_key,
                            algorithms=["RS256"],
                            options={"verify_aud": False},
                            #audience=[settings.KEYCLOAK_CLIENT_ID, "account"],
                            )
        print(f"Decoded Token: {payload}")

        #return payload
        return{
           "sub": payload.get("sub"),
            "username": payload.get("preferred_username"),
            "refresh_token": token,  # Pass refresh token for logout,
            "roles": payload.get("realm_access", {}).get("roles", []),
       }

    except JWTError as e:
        #raise HTTPException(status_code=401, detail=f"Invalid or expired token:{str(e)}")
        logger.error(f"Token verification failed: {e.args}")

async def check_user_role(token: str, required_roles: list):
    payload = await verify_token(token)

    # Extract roles from Keycloak token
    # roles = payload.get("realm_access", {}).get("roles", [])
    roles = payload.get("roles", [])
    if not any(role in roles for role in required_roles):
        raise HTTPException(status_code=403, detail="Access denied: Insufficient permissions")
    
    