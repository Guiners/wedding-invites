from __future__ import annotations

from pydantic import BaseModel


class InvitationIn(BaseModel):
    invitation_model: str
    additional_card: str
    envelope_color: str
    envelope_personalization: bool | None = None
    envelope_wax_seal: bool | None = None
    envelope_ribbon: bool | None = None
    envelope_foil_stamping: bool | None = None
    song_link: str
