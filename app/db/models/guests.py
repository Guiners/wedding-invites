from __future__ import annotations

import typing

from sqlalchemy import BigInteger, Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import Base

if typing.TYPE_CHECKING:
    from app.db.models.projects import Project


class Guests(Base):
    __tablename__ = "guests"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    project_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )

    invited_guests: Mapped[str] = mapped_column(String(255), nullable=False)
    special_invitation: Mapped[str] = mapped_column(String(255))
    with_plus_one: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    with_children: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    with_accommodation: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )
    # relationship
    project: Mapped["Project"] = relationship(
        back_populates="guests",
        uselist=False,
    )
