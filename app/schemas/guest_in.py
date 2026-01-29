from __future__ import annotations

from pydantic import BaseModel


class GuestIn(BaseModel):
    invited_guests: str
    special_invitation: str | None = None
    with_plus_one: bool | None = None
    with_children: bool | None = None
    with_accommodation: bool | None = None
    code: str
