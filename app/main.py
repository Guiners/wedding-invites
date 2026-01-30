from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request, status
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.db_handler import DbHandler
from app.constants import BASE_DIR, INVITES_MODEL_HASH, INVITES_MODEL_TEMPLATES
from app.db.database import get_db
from app.tools import logger

app = FastAPI(title="Weddings Invitation")
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

wedding_date_iso = "2026-07-26"
wedding_date_human = "26 lipca 2026 dupa"
wedding_date_time = "2026-07-26T16:30"


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse(
        "invitation_base1.html",
        {
            "request": request,
            "wedding_date_iso": wedding_date_iso,
            "wedding_date_human": wedding_date_human,
            "wedding_date_time": wedding_date_time,
        },
    )




# @app.get("id/{project_id}", status_code=status.HTTP_200_OK, response_class=HTMLResponse)

@app.get("/{invite_model}/{code}/{client_name}", status_code=status.HTTP_200_OK, response_class=HTMLResponse)
async def generate_invitation(request: Request,
        code: str, client_name: str, invite_model: str,
        db: AsyncSession = Depends(get_db),):

    try:
        decoded_invitation_model = INVITES_MODEL_HASH[invite_model]
        invitation_template = INVITES_MODEL_TEMPLATES[decoded_invitation_model]

    except KeyError:
        logger.error(f"Invalid invite model: {invite_model}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


    try:
        wedding_data = await DbHandler(db).get_event_with_code_and_client(code, client_name)
    except Exception as err:
        logger.error(f"App failed while pulling data from DB: {err}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return templates.TemplateResponse(
        invitation_template,
        {
            "request": request,
            "wedding_date_iso": wedding_data.event.wedding_date_iso,
            "wedding_date_human": wedding_data.event.wedding_date_human,
            "wedding_date_time": wedding_data.event.wedding_date_time,
        },
    )

