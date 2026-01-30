from __future__ import annotations

from pydantic import BaseModel, field_validator

from app.constants import PL_MAP


class ProjectIn(BaseModel):
    client_name: str
    code: str

    @field_validator("client_name", mode="before")
    @classmethod
    def remove_polish_chars(cls, _string: str) -> str:
        return _string.translate(PL_MAP)
