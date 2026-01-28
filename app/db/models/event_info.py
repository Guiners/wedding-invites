from __future__ import annotations

import typing
from datetime import date, time

from sqlalchemy import BigInteger, Boolean, Date, ForeignKey, String, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import Base

if typing.TYPE_CHECKING:
    from app.db.models.projects import Project


class EventInfo(Base):
    __tablename__ = "event_info"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    project_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )

    brides_first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    brides_last_name: Mapped[str] = mapped_column(String(255), nullable=False)
    brides_phone_number: Mapped[str] = mapped_column(String(255), nullable=False)

    grooms_first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    grooms_last_name: Mapped[str] = mapped_column(String(255), nullable=False)
    grooms_phone_number: Mapped[str] = mapped_column(String(255), nullable=False)

    wedding_date: Mapped[date] = mapped_column(Date, nullable=False)
    wedding_time: Mapped[time] = mapped_column(Time, nullable=False)
    rsvp_deadline_date: Mapped[date] = mapped_column(Date, nullable=False)

    name_of_the_church: Mapped[str] = mapped_column(String(255), nullable=False)
    church_address: Mapped[str] = mapped_column(String(255), nullable=False)

    name_of_the_wedding_venue: Mapped[str] = mapped_column(String(255), nullable=False)
    wedding_venue_address: Mapped[str] = mapped_column(String(255), nullable=False)

    flowers_or_alcohol: Mapped[str] = mapped_column(String(255), nullable=False)
    gifts_or_cash: Mapped[str] = mapped_column(String(255), nullable=False)

    children_be_invited: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    # relationship
    project: Mapped["Project"] = relationship(
        back_populates="event_info",
        uselist=False,
    )
