from uuid import uuid4, UUID
from datetime import datetime
from app.services.cassandra_service import CassandraService
from app.models.enrollments import CreateEnrollmentRequest, Enrollment

class EnrollmentService:
    def __init__(self):
        self.cassandra = CassandraService()

    async def create_enrollment(self, request: CreateEnrollmentRequest) -> dict:
        enrollment = Enrollment(
            enrollment_id=uuid4(),
            student_id=request.student_id,
            semester=request.semester,
            enrolled_at=datetime.utcnow()
        )

        await self.cassandra.create_enrollment(enrollment)

        return {
            "enrollment_id": str(enrollment.enrollment_id),
            "student_id": str(enrollment.student_id),
            "enrolled_at": enrollment.enrolled_at.isoformat()
        }
    async def delete_by_student_and_semester(self, student_id: UUID, semester: str) -> dict:
        success = await self.cassandra.delete_enrollments_by_student_and_semester(student_id, semester)
        if not success:
            raise Exception("Failed to delete enrollments")
        return {
            "message": f"Enrollments for student {student_id} in semester '{semester}' have been deleted."
        }