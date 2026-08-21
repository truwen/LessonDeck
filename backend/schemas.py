from pydantic import BaseModel, ConfigDict


class CourseCreate(BaseModel):
    name: str
    subject: str
    grade_level: str
    period: str | None = None


class CourseUpdate(BaseModel):
    name: str
    subject: str
    grade_level: str
    period: str | None = None


class CourseResponse(CourseCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ScheduleCreate(BaseModel):
    day_type: str
    period_label: str
    start_time: str
    end_time: str
    course_id: int | None = None


class ScheduleUpdate(BaseModel):
    day_type: str
    period_label: str
    start_time: str
    end_time: str
    course_id: int | None = None


class ScheduleResponse(ScheduleCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)