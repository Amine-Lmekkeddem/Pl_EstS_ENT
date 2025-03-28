from fastapi import Request, HTTPException
from fastapi.routing import APIRoute
from app.utils.keycloak import verify_token

class AuthMiddleware(APIRoute):
    def get_route_handler(self):
        original_handler = super().get_route_handler()

        async def custom_handler(request: Request):
            if "/protected" in request.url.path:
                token = request.headers.get("Authorization")
                if not token or not token.startswith("Bearer "):
                    raise HTTPException(status_code=401, detail="Token missing or invalid")
                await verify_token(token.split(" ")[1])

            return await original_handler(request)

        return custom_handler
