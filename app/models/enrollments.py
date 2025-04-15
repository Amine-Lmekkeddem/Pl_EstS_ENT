from pydantic import BaseModel
import datetime
from uuid import UUID

class CreateEnrollmentRequest(BaseModel):
    student_id: UUID
    semester: str  # Semester in which the student is enrolling

class Enrollment(CreateEnrollmentRequest):
    enrollment_id: UUID
    enrolled_at: datetime.datetime  # Timestamp for when the user enrolled in the course
