from __future__ import annotations

from datetime import date, datetime, time
from typing import Any

from pydantic import BaseModel, field_serializer, field_validator


class EventIn(BaseModel):
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
    children_be_invited: bool | None = None

    @field_validator("grooms_phone_number", "brides_phone_number", mode="before")
    @classmethod
    def phone_to_str(cls, value: Any) -> str:
        return str(value)

    @field_validator("wedding_date", "rsvp_deadline_date", mode="before")
    @classmethod
    def parse_polish_date(cls, value: Any) -> date:
        if isinstance(value, date) and not isinstance(value, datetime):
            return value
        if isinstance(value, datetime):
            return value.date()
        if isinstance(value, str):
            value = value.strip()
            for fmt in ("%d.%m.%Y", "%d-%m-%Y", "%Y-%m-%d"):
                try:
                    return datetime.strptime(value, fmt).date()
                except ValueError:
                    pass
            raise ValueError(f"Unsupported date string format: {value!r}")
        raise TypeError(f"Unsupported date value: {value!r}")

    @field_validator("wedding_time", mode="before")
    @classmethod
    def parse_time(cls, value: Any) -> time:
        if isinstance(value, time):
            return value
        if isinstance(value, datetime):
            return value.time()
        if isinstance(value, str):
            value = value.strip()
            return datetime.strptime(value, "%H:%M").time()
        raise TypeError(f"Unsupported time value: {value!r}")
