from __future__ import annotations

import typing

from sqlalchemy import BigInteger, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.models.base import Base

if typing.TYPE_CHECKING:
    from app.db.models.event_info import EventInfo
    from app.db.models.guests import Guests
    from app.db.models.invitation_info import InvitationInfo


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
    )

    client_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    code: Mapped[str] = mapped_column(
        String(8),
        nullable=False,
        unique=True,
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime,
        default=func.now(),
        nullable=False,
    )

    # relationships
    event_info: Mapped["EventInfo"] = relationship(
        back_populates="project",
        uselist=False,
    )

    invitation_info: Mapped["InvitationInfo"] = relationship(
        back_populates="project",
        uselist=False,
    )

    guests: Mapped["Guests"] = relationship(
        back_populates="project",
        uselist=False,
    )
