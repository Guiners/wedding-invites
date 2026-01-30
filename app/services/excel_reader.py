import random
import string
from pathlib import Path
from typing import Any

import pandas as pd

from app.constants import (EVENT_COL_MAP, EXCEL_SHEET_NAMES_MAP,
                           GUESTS_COL_MAP, INVITATION_COL_MAP)
from app.schemas.event_in import EventIn
from app.schemas.guest_in import GuestIn
from app.schemas.invitation_in import InvitationIn
from app.schemas.project_in import ProjectIn
from app.tools.logger import logger

excel_path_ = "../db/excel_files/Dummy Invite Sheet V1.xlsx"


class ExcelReader:
    def __init__(self, excel_path: Path):
        self.excel_path = excel_path
        self.invitation_orm = self.get_invitation_data()
        self.event_orm = self.get_event_data()
        self.guests_list_orm = self.get_guest_data()
        self.project_orm = self.get_project_data()

    @staticmethod
    def generate_code() -> str:
        return "".join(random.choices(string.ascii_lowercase + string.digits, k=8))

    @staticmethod
    def empty_checker(df: pd.DataFrame):
        if df.empty:
            raise ValueError("Sheet is empty")

    def normalize_dict(self, data: dict):
        for key, value in data.items():
            value = self.normalize_nan(value)
            value = self.normalize_bool(value)
            data[key] = value

    @staticmethod
    def normalize_nan(value: Any):
        if isinstance(value, float) and value != value:  # NaN
            return None
        return value

    @staticmethod
    def normalize_bool(value: Any):
        if value in ("Tak", "TAK", "Yes", True):
            return True
        if value in ("Nie", "NIE", "No", False):
            return False
        return value

    def read_excel_sheet(self, sheet_name: str, headers: dict):
        df = pd.read_excel(self.excel_path, sheet_name=sheet_name)
        self.empty_checker(df)
        logger.debug("Read RAW Excel sheet: \n%s", df)
        df = df.rename(columns=headers)
        logger.debug("Renamed columns in Excel sheet: \n%s", df.columns)
        return df

    def get_data_for_orm(self, data, model):
        self.normalize_dict(data)
        validated_data = model.model_validate(data)
        return validated_data.model_dump(exclude_none=True, mode="python")

    def handle_guests(self, data: list[dict]):
        guests_list = []
        for single_guests in data:
            single_guests["code"] = self.generate_code()
            guest_orm = self.get_data_for_orm(single_guests, GuestIn)
            guests_list.append(guest_orm)
        return guests_list

    def get_invitation_data(self):
        invitation_sheet_df = self.read_excel_sheet(
            EXCEL_SHEET_NAMES_MAP["invitation_sheet"], INVITATION_COL_MAP
        )
        return self.get_data_for_orm(
            invitation_sheet_df.iloc[0].to_dict(), InvitationIn
        )

    def get_event_data(self):
        event_sheet_df = self.read_excel_sheet(
            EXCEL_SHEET_NAMES_MAP["event_sheet"], EVENT_COL_MAP
        )
        return self.get_data_for_orm(event_sheet_df.iloc[0].to_dict(), EventIn)

    def get_guest_data(self):
        guests_sheet_df = self.read_excel_sheet(
            EXCEL_SHEET_NAMES_MAP["guests_sheet"], GUESTS_COL_MAP
        )
        guests_data = guests_sheet_df.to_dict(orient="records")
        return self.handle_guests(guests_data)

    def get_project_data(self):
        client_name = (
            f"{self.event_orm['brides_first_name']}-"
            f"{self.event_orm['brides_last_name']}-and-"
            f"{self.event_orm['grooms_first_name']}-"
            f"{self.event_orm['grooms_last_name']}-"
            f"{self.event_orm['wedding_date'].strftime('%d-%m-%Y')}"
        )
        project_orm = ProjectIn.model_validate(
            {
                "client_name": client_name,
                "code": self.generate_code(),
            }
        )
        return project_orm.model_dump(exclude_none=True, mode="python")

    def generate_invite_link(self):
        ...