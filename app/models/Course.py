from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class CreateCourseRequest(BaseModel):
    title: str
    description: str
    category: str
    course_semester: str
    teacher_id: UUID

class course(CreateCourseRequest):
    course_id: UUID
    created_at: datetime
