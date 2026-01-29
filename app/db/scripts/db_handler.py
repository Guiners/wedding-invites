from sqlalchemy.ext.asyncio import AsyncSession

from app.db.scripts.excel_reader import ExcelReader

class DbHandler:
    def __init__(self, db: AsyncSession):
        self.db = db