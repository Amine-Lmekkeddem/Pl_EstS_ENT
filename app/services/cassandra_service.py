# app/services/cassandra_service.py
from cassandra.cluster import Cluster
from app.config import settings
from app.models.user import user
from uuid import UUID
from datetime import datetime
from app.models import Course
class CassandraService:
    def __init__(self):
        self.cluster = Cluster(["localhost"], port=9042)
        self.session = self.cluster.connect("education_platform")
        # Prepare user insert
        self.prepared_insert = self.session.prepare("""
            INSERT INTO users (
                user_id, username, email, role, student_number,
                department, profile_picture, status, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            
        """)
        # Prepare delete statements
        self.prepared_delete_user = self.session.prepare("""
            DELETE FROM users WHERE user_id = ?
        """)
        # Prepare course insert
        self.prepared_insert_course = self.session.prepare("""
            INSERT INTO courses (
                course_id, title, description, category, course_semester, teacher_id, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """)
        self.prepared_delete_course = self.session.prepare("""
            DELETE FROM courses WHERE course_id = ?
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
    # function for deleting user from cassandra
    async def delete_user(self, user_id: UUID) -> bool:
        """Delete a user from Cassandra"""
        try:
            self.session.execute(self.prepared_delete_user, (user_id,))
            return True
        except Exception:
            return False
    
    async def create_course(self, course_data: Course) -> Course:
        self.session.execute(self.prepared_insert_course, (
            course_data.course_id,
            course_data.title,
            course_data.description,
            course_data.category,
            course_data.course_semester,
            course_data.teacher_id,
            course_data.created_at
        ))
        return course_data
    # function for deleting course from cassandra
    async def delete_course(self, course_id: UUID) -> bool:
        """Delete a course from Cassandra"""
        try:
            self.session.execute(self.prepared_delete_course, (course_id,))
            return True
        except Exception:
            return False 
    def __del__(self):
        """Clean up connection when service is destroyed"""
        self.cluster.shutdown()