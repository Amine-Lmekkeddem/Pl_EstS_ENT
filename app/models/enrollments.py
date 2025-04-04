from pydantic import BaseModel
import datetime

class enrollment(BaseModel):
    id: int
    Semester: str
    enrolled_at: datetime.datetime  # Timestamp for when the user enrolled in the course
    student_is : str 