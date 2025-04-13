# app/services/course_service.py

from uuid import uuid4, UUID
from datetime import datetime
from app.services.cassandra_service import CassandraService
from app.models.Course import course, CreateCourseRequest  # you’ll define CreateCourseRequest too

class CourseService:
    def __init__(self):
        self.cassandra = CassandraService()

    async def create_course(self, course_request: CreateCourseRequest) -> dict:
        """Insert course into Cassandra"""

        course_data = course(
            course_id=uuid4(),
            title=course_request.title,
            description=course_request.description,
            category=course_request.category,
            course_semester=course_request.course_semester,
            teacher_id=course_request.teacher_id,
            created_at=datetime.utcnow()
        )

        await self.cassandra.create_course(course_data)

        return {
            "course_id": str(course_data.course_id),
            "title": course_data.title,
            "created_at": course_data.created_at.isoformat()
        }
    
    async def delete_course(self, course_id: UUID) -> dict:
        """
        Delete a course from Cassandra
        Returns:
            {
                "success": bool,
                "course_id": str,
                "message": str
            }
        """
        try:
            success = await self.cassandra.delete_course(course_id)
            if not success:
                raise Exception("Failed to delete course")
            
            return {
                "success": True,
                "course_id": str(course_id),
                "message": "Course deleted successfully"
            }
        except Exception as e:
            return {
                "success": False,
                "course_id": str(course_id),
                "message": f"Error deleting course: {str(e)}"
            }