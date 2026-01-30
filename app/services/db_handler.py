from pathlib import Path

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload
from starlette.responses import JSONResponse

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

            logger.info(f"INSERTED: {project}")

            logger.info(f"project.id = {project.id}")
            logger.info(f"client_name = {project.client_name}")
            logger.info(f"code = {project.code}")

            fresh = await self.db.scalar(select(Project).where(Project.id == project.id))
            logger.info(f"FOUND IN DB: {fresh is not None}")
            return project

        except Exception as err:
            logger.error("ERROR DURING FILLING DB WITH EXCEL FILE ", err)


    async def get_event_with_code_and_client(self, code: str, client_name: str):
        stmt = (
            select(Project)
            .options(
                joinedload(Project.event)
            ).where((Project.code == code) & (Project.client_name == client_name))

        )
        raw_project_data= (await self.db.execute(stmt)).scalar_one_or_none()
        return ProjectOut.model_validate(raw_project_data)

        # return project

        # return JSONResponse(content=jsonable_encoder(project))



    async def _execute_ddl(self, stmt: str) -> None:
        """
        Execute a raw SQL DDL statement.

        Args:
            stmt (str): The SQL statement to execute.

        Returns:
            None
        """
        await self.db.execute(text(stmt))
        await self.db.commit()
        logger.info("DDL executed successfully")