import datetime
from rzd.database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, text, ForeignKey, Date
from sqlalchemy.orm import relationship, Mapped, mapped_column


class Users(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True, nullable=False, index=True)
    u_name: Mapped[str] = mapped_column(nullable=False)

    work_hours: Mapped[list["User_Work_sessions"]] = relationship(back_populates="usr")

    user_wd: Mapped[list["Work_day"]] = relationship(
        back_populates="user_work_day",
        secondary="user_work_sessions"
    )

class User_Work_sessions(Base):
    __tablename__ = 'user_work_sessions'

    date_id: Mapped[int] = mapped_column(ForeignKey("work_day.wd_id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), primary_key=True)
    work_hour: Mapped[int]

    usr: Mapped[list["Users"]] = relationship(back_populates="work_hours")

    date: Mapped[list["Work_day"]] = relationship(back_populates="ses")
    
    

class Work_day(Base):
    __tablename__ = 'work_day'

    wd_id: Mapped[int] = mapped_column(primary_key=True, nullable=False, index=True)
    day: Mapped[datetime.datetime] = mapped_column(nullable=False)

    user_work_day: Mapped[list["Users"]] = relationship(
        back_populates="user_wd",
        secondary="user_work_sessions"
    )

    ses: Mapped[list["User_Work_sessions"]] = relationship(back_populates='date')