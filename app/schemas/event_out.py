from __future__ import annotations

from datetime import date, time, datetime
from app.constants import POLISH_MONTHS
from pydantic import BaseModel, computed_field, model_validator, field_validator


class EventOut(BaseModel):
    id: int
    project_id: int
    brides_first_name: str
    brides_last_name: str
    brides_phone_number: str

    grooms_first_name: str
    grooms_last_name: str
    grooms_phone_number: str

    wedding_date: date
    wedding_time: time
    rsvp_deadline_date: date

    name_of_the_church: str
    church_address: str

    name_of_the_wedding_venue: str
    wedding_venue_address: str

    flowers_or_alcohol: str
    gifts_or_cash: str
    children_be_invited: bool

    model_config = {"from_attributes": True}

    @computed_field
    @property
    def wedding_date_iso (self) -> str:
        return self.wedding_date.strftime("%Y-%m-%d")

    @computed_field
    @property
    def wedding_date_human (self) -> str:
        return (
            f"{self.wedding_date.day} "
            f"{POLISH_MONTHS[self.wedding_date.month]} "
            f"{self.wedding_date.year}"
        )

    @computed_field
    @property
    def wedding_date_time (self) -> str:
        wedding_date_time = datetime.combine(self.wedding_date, self.wedding_time)
        return wedding_date_time.strftime("%Y-%m-%dT%H:%M")
