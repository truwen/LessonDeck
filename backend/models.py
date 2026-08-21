from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database import Base


class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    subject: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    grade_level: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    period: Mapped[str] = mapped_column(
        String(50),
        nullable=True,
    )

    schedules: Mapped[list["ScheduleEntry"]] = relationship(
        back_populates="course"
    )


class ScheduleEntry(Base):
    __tablename__ = "schedule_entries"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    day_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    period_label: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    start_time: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
    )

    end_time: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
    )

    course_id: Mapped[int | None] = mapped_column(
        ForeignKey("courses.id"),
        nullable=True,
    )

    course: Mapped["Course | None"] = relationship(
        back_populates="schedules"
    )