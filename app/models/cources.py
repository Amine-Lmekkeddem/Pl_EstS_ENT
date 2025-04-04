import datetime
from pydantic import BaseModel

class course(BaseModel):
    title : str 
    course_description : str 
    category : str 
    course_semester : str 
    course_instructor : str 
    created_at : datetime.datetime  # Timestamp for when the course was created
    