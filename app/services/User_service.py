# app/services/user_service.py
from uuid import UUID
from datetime import datetime
from app.services.cassandra_service import CassandraService
from app.services.keycloak_admin import create_user_in_keycloak, delete_user_from_keycloak
from app.models.user import CreateUserRequest, user

class UserService:
    def __init__(self):
        self.cassandra = CassandraService()

    async def create_user(self, user_request: CreateUserRequest) -> dict:
        """Orchestrate user creation across both systems"""
        try:
            student_number_str = str(user_request.student_number)

            # 1. Create in Keycloak
            keycloak_result = await create_user_in_keycloak(
                username=user_request.username,
                email=user_request.email,
                role=user_request.role,
                temp_password=user_request.temporary_password or self._generate_temp_password()
            )

            # 2. Prepare Cassandra record
            db_user = user(
            id=UUID(keycloak_result["user_id"]),
            username=user_request.username,
            email=user_request.email,
            role=user_request.role,
            student_number=user_request.student_number,  # Now a string
            department=user_request.department,
            profile_picture=user_request.profile_picture,
            status=user_request.status,
            created_at=datetime.utcnow()
        )

            # 3. Save to Cassandra
            await self.cassandra.create_user(db_user)

            return {
                "user_id": str(db_user.id),
                "username": db_user.username,
                "created_at": db_user.created_at.isoformat()
            }

        except Exception as e:
            # Rollback Keycloak if Cassandra fails
            if 'keycloak_result' in locals():
                await delete_user_from_keycloak(keycloak_result["user_id"])
            raise

    def _generate_temp_password(self) -> str:
        """Generate a random temporary password"""
        import secrets
        import string
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        return ''.join(secrets.choice(chars) for _ in range(12))