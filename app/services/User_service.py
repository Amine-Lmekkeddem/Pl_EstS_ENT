# app/services/user_service.py
from uuid import UUID
from datetime import datetime
from app.services.cassandra_service import CassandraService
from app.services.keycloak_admin import create_user_in_keycloak, delete_user_from_keycloak
from app.models.user import CreateUserRequest, user
from fastapi import HTTPException
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
    async def delete_user(self, user_id: UUID) -> dict:
        """
        Delete user from both systems with rollback support
        Returns:
            {
                "success": bool,
                "user_id": str,
                "systems": {
                    "keycloak": bool,
                    "cassandra": bool
                },
                "message": str
            }
        """
        result = {
            "success": True,
            "user_id": str(user_id),
            "systems": {
                "keycloak": False,
                "cassandra": False
            },
            "message": "Deletion started"
        }

        try:
            # 1. Delete from Keycloak first
            try:
                await delete_user_from_keycloak(str(user_id))
                result["systems"]["keycloak"] = True
            except Exception as keycloak_error:
                raise HTTPException(
                    status_code=502,
                    detail=f"Keycloak deletion failed: {str(keycloak_error)}"
                )

            # 2. Delete from Cassandra
            try:
                cassandra_success = await self.cassandra.delete_user(user_id)
                if not cassandra_success:
                    raise Exception("Cassandra deletion failed")
                result["systems"]["cassandra"] = True
            except Exception as cassandra_error:
                # Attempt to recreate in Keycloak if Cassandra fails
                if result["systems"]["keycloak"]:
                    await self._recreate_keycloak_user(user_id)
                raise HTTPException(
                    status_code=500,
                    detail=f"Cassandra deletion failed: {str(cassandra_error)}"
                )

            result["message"] = "User deleted successfully"
            return result

        except HTTPException as http_error:
            result.update({
                "success": False,
                "message": http_error.detail
            })
            return result

        except Exception as e:
            result.update({
                "success": False,
                "message": f"Unexpected error: {str(e)}"
            })
            return result

    async def _recreate_keycloak_user(self, user_id: UUID):
        """Rollback: Recreate Keycloak user if Cassandra deletion fails"""
        # Implement based on your user recovery requirements
        # Could fetch from backup cache or secondary datastore
        pass
    def _generate_temp_password(self) -> str:
        """Generate a random temporary password"""
        import secrets
        import string
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        return ''.join(secrets.choice(chars) for _ in range(12))