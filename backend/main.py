from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from backend.database import Base, engine, get_db
from backend.models import Course, ScheduleEntry
from backend.schemas import (
    CourseCreate,
    CourseResponse,
    CourseUpdate,
    ScheduleCreate,
    ScheduleResponse,
    ScheduleUpdate,
)


app = FastAPI(title="LessonDeck")

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "app": "LessonDeck",
    }


@app.get(
    "/api/courses",
    response_model=list[CourseResponse],
)
def get_courses(
    db: Session = Depends(get_db),
):
    return db.query(Course).order_by(Course.id).all()


@app.post(
    "/api/courses",
    response_model=CourseResponse,
)
def create_course(
    course: CourseCreate,
    db: Session = Depends(get_db),
):
    new_course = Course(
        name=course.name,
        subject=course.subject,
        grade_level=course.grade_level,
        period=course.period,
    )

    db.add(new_course)
    db.commit()
    db.refresh(new_course)

    return new_course


@app.put(
    "/api/courses/{course_id}",
    response_model=CourseResponse,
)
def update_course(
    course_id: int,
    course: CourseUpdate,
    db: Session = Depends(get_db),
):
    existing_course = db.get(Course, course_id)

    if not existing_course:
        raise HTTPException(
            status_code=404,
            detail="Course not found.",
        )

    existing_course.name = course.name
    existing_course.subject = course.subject
    existing_course.grade_level = course.grade_level
    existing_course.period = course.period

    db.commit()
    db.refresh(existing_course)

    return existing_course


@app.delete("/api/courses/{course_id}")
def delete_course(
    course_id: int,
    db: Session = Depends(get_db),
):
    existing_course = db.get(Course, course_id)

    if not existing_course:
        raise HTTPException(
            status_code=404,
            detail="Course not found.",
        )

    assigned_entries = (
        db.query(ScheduleEntry)
        .filter(ScheduleEntry.course_id == course_id)
        .count()
    )

    if assigned_entries > 0:
        raise HTTPException(
            status_code=409,
            detail=(
                "This class is assigned to schedule entries. "
                "Remove or reassign those entries first."
            ),
        )

    db.delete(existing_course)
    db.commit()

    return {"status": "deleted"}


@app.get(
    "/api/schedule",
    response_model=list[ScheduleResponse],
)
def get_schedule(
    db: Session = Depends(get_db),
):
    return (
        db.query(ScheduleEntry)
        .order_by(
            ScheduleEntry.day_type,
            ScheduleEntry.start_time,
        )
        .all()
    )


@app.post(
    "/api/schedule",
    response_model=ScheduleResponse,
)
def create_schedule_entry(
    entry: ScheduleCreate,
    db: Session = Depends(get_db),
):
    if entry.end_time <= entry.start_time:
        raise HTTPException(
            status_code=400,
            detail="End time must be after start time.",
        )

    new_entry = ScheduleEntry(
        day_type=entry.day_type,
        period_label=entry.period_label,
        start_time=entry.start_time,
        end_time=entry.end_time,
        course_id=entry.course_id,
    )

    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)

    return new_entry


@app.put(
    "/api/schedule/{entry_id}",
    response_model=ScheduleResponse,
)
def update_schedule_entry(
    entry_id: int,
    entry: ScheduleUpdate,
    db: Session = Depends(get_db),
):
    existing_entry = db.get(
        ScheduleEntry,
        entry_id,
    )

    if not existing_entry:
        raise HTTPException(
            status_code=404,
            detail="Schedule entry not found.",
        )

    if entry.end_time <= entry.start_time:
        raise HTTPException(
            status_code=400,
            detail="End time must be after start time.",
        )

    existing_entry.day_type = entry.day_type
    existing_entry.period_label = entry.period_label
    existing_entry.start_time = entry.start_time
    existing_entry.end_time = entry.end_time
    existing_entry.course_id = entry.course_id

    db.commit()
    db.refresh(existing_entry)

    return existing_entry


@app.delete("/api/schedule/{entry_id}")
def delete_schedule_entry(
    entry_id: int,
    db: Session = Depends(get_db),
):
    existing_entry = db.get(
        ScheduleEntry,
        entry_id,
    )

    if not existing_entry:
        raise HTTPException(
            status_code=404,
            detail="Schedule entry not found.",
        )

    db.delete(existing_entry)
    db.commit()

    return {"status": "deleted"}