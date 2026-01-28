from __future__ import annotations

import typing

from sqlalchemy import BigInteger, Boolean, Date, ForeignKey, String, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import Base

if typing.TYPE_CHECKING:
    from app.db.models.projects import Project


class InvitationInfo(Base):
    __tablename__ = "invitation_info"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    project_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )

    invitation_model: Mapped[str] = mapped_column(String(255))
    additional_card: Mapped[str] = mapped_column(String(255))

    envelope_color: Mapped[str] = mapped_column(String(255), nullable=False)

    envelope_personalization: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )
    envelope_wax_seal: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )
    envelope_ribbon: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )
    envelope_foil_stamping: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )
    song_link: Mapped[str] = mapped_column(String(255))

    # relationship
    project: Mapped["Project"] = relationship(
        back_populates="invitation_info",
        uselist=False,
    )
