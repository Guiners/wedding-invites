import asyncio
from pathlib import Path

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload
from starlette.responses import JSONResponse
from app.constants import DOMAIN, INVITES_MODEL_HASH
from app.db.database import get_db
from app.db.models.event import Event
from app.db.models.guests import Guests
from app.db.models.invitation import Invitation
from app.db.models.projects import Project
from app.schemas.project_out import ProjectOut
from app.services.excel_reader import ExcelReader
from app.tools import logger

# stmt = (  #stmt do wyjecia wszystkiego z bazy, kazdej tabeli
#     select(Project)
#     .options(
#         joinedload(Project.event),  # albo Project.event_info
#         joinedload(Project.invitation),  # albo Project.invitation_info
#         selectinload(Project.guests),
#     )
# )


class DbHandler:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_full_project(
        self,
        project_orm: dict,
        guests_list_orm: list[dict],
        event_orm: dict,
        invitation_orm: dict,
    ) -> Project:

        project = Project(**project_orm)

        project.event = Event(**event_orm, project=project)
        project.invitation = Invitation(**invitation_orm, project=project)

        project.guests = [Guests(**guest_dict) for guest_dict in guests_list_orm]

        self.db.add(project)
        await self.db.commit()
        await self.db.refresh(project)
        stmt = (
            select(Project)
            .where(Project.id == project.id)
            .options(
                joinedload(Project.invitation),
                joinedload(Project.event),
                selectinload(Project.guests),
            )
        )
        project = (await self.db.execute(stmt)).scalar_one()

        return project


    async def fill_db(self, excel_path: Path):
        try:
            logger.info(f"LOADING EXCEL FILE FROM: {excel_path}")
            excel_data = ExcelReader(excel_path)

            project = await self.create_full_project(
                excel_data.project_orm,
                excel_data.guests_list_orm,
                excel_data.event_orm,
                excel_data.invitation_orm,
            )

            logger.debug(f"INSERTED: {project}")

            logger.debug(f"project.id = {project.id}")
            logger.debug(f"client_name = {project.client_name}")
            logger.debug(f"code = {project.code}")
            logger.debug(f"invitation_model = {project.invitation.invitation_model}")

            return project

        except Exception as err:
            logger.error(f"ERROR DURING FILLING DB WITH EXCEL FILE {err}")

    @staticmethod
    def generate_link(project: Project):
        model_code = next(k for k, v in INVITES_MODEL_HASH.items() if v == project.invitation.invitation_model)
        return f"{DOMAIN}/{model_code}/{project.code}/{project.client_name}"


    async def get_event_with_code_and_client(self, code: str, client_name: str):
        stmt = (
            select(Project)
            .options(
                joinedload(Project.event)
            ).where((Project.code == code) & (Project.client_name == client_name))
        )  #todo 2x stmt w kodzie

        raw_project_data= (await self.db.execute(stmt)).scalar_one_or_none()
        return ProjectOut.model_validate(raw_project_data)


async def main() -> None:
    # excel_path = "../db/excel_files/Dummy Invite Sheet V1.xlsx" #tu trzeba dodac bazujac na BASE DIR
    BASE_DIR = Path(__file__).resolve().parent.parent  # /app/app
    excel_path = BASE_DIR / "db" / "excel_files" / "Dummy Invite Sheet V1.xlsx" #todo przepisac
    async for db in get_db():
        handler = DbHandler(db)
        project = await handler.fill_db(excel_path)
        link = handler.generate_link(project)
        logger.info(f"Link to invite: {link}")


if __name__ == "__main__":
    asyncio.run(main()) ##todo napisac to tak, zeby odpalac to przez sciezke
    # i albo uploadowac to na jakiegos drive albo po prostu przesylac na serwer (idk jak taki host dziala)
    # moze zrobic panel admina i tam dac mozliwosc wrzucenia pliku
