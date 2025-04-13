# app/services/cassandra_service.py
from cassandra.cluster import Cluster
from app.config import settings
from app.models.user import user
from uuid import UUID
from datetime import datetime

class CassandraService:
    def __init__(self):
        self.cluster = Cluster(["localhost"], port=9042)
        self.session = self.cluster.connect("education_platform")
        self.prepared_insert = self.session.prepare("""
            INSERT INTO users (
                user_id, username, email, role, student_number,
                department, profile_picture, status, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            
        """)

    async def create_user(self, user_data: user) -> user:
        """Insert a user into Cassandra"""
        self.session.execute(self.prepared_insert, (
            user_data.id,
            user_data.username,
            user_data.email,
            user_data.role,
            user_data.student_number,
            user_data.department,
            user_data.profile_picture,
            user_data.status,
            user_data.created_at
        ))
        return user_data

    def __del__(self):
        """Clean up connection when service is destroyed"""
        self.cluster.shutdown()