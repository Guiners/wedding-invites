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
from app.tools.google_handler import google_maps_link_generator
app = FastAPI(title="Weddings Invitation")
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# wedding_date_iso = "2026-07-26"
# wedding_date_human = "26 lipca 2026 dupa"
# wedding_date_time = "2026-07-26T16:30"
#
#
# @app.get("/")
# def index(request: Request):
#     return templates.TemplateResponse(
#         "invitation_base1.html",
#         {
#             "request": request,
#             "wedding_date_iso": wedding_date_iso,
#             "wedding_date_human": wedding_date_human,
#             "wedding_date_time": wedding_date_time,
#         },
#     )


# @app.get("/{invitation_model}/{code}/{client_name}", status_code=status.HTTP_200_OK, response_class=HTMLResponse)
# async def generate_invitation(request: Request,
#                               code: str, client_name: str, invitation_model: str,
#                               db: AsyncSession = Depends(get_db), ):
#     try:
#         decoded_invitation_model = INVITES_MODEL_HASH[invitation_model]
#         invitation_template = INVITES_MODEL_TEMPLATES[decoded_invitation_model]
#
#     except KeyError:
#         logger.error(f"Invalid invite model: {invitation_model}")
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
#
#     try:
#
#         wedding_data = await DbHandler(db).get_event_with_id_and_client(code, client_name)
#     except Exception as err:
#         logger.error(f"App failed while pulling data from DB: {err}")
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
#
#     church_google_maps_link = google_maps_link_generator(wedding_data.event.name_of_the_church,
#                                                          wedding_data.event.church_address)
#     venue_google_maps_link = google_maps_link_generator(wedding_data.event.name_of_the_wedding_venue,
#                                                         wedding_data.event.wedding_venue_address)
#
#     template_data = {
#         "request": request,
#         "church_google_maps_link": church_google_maps_link,
#         "venue_google_maps_link": venue_google_maps_link,
#         "wedding_date_iso": wedding_data.event.wedding_date_iso,
#         "wedding_date_human": wedding_data.event.wedding_date_human,
#         "wedding_date_time": wedding_data.event.wedding_date_time,
#     }
#
#     return templates.TemplateResponse(
#         invitation_template,
#         template_data
#     )
@app.get("/{invitation_model}/{_id}/{client_name}", status_code=status.HTTP_200_OK, response_class=HTMLResponse)
async def generate_invitation(request: Request,
                              _id: int, client_name: str, invitation_model: str,
                              db: AsyncSession = Depends(get_db), ):

    try:
        decoded_invitation_model = INVITES_MODEL_HASH[invitation_model]
        invitation_template = INVITES_MODEL_TEMPLATES[decoded_invitation_model]

    except KeyError:
        logger.error(f"Invalid invite model: {invitation_model}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


    try:

        wedding_data = await DbHandler(db).get_event_with_id_and_client(_id, client_name)
    except Exception as err:
        logger.error(f"App failed while pulling data from DB: {err}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    church_google_maps_link = google_maps_link_generator(wedding_data.event.name_of_the_church, wedding_data.event.church_address)
    venue_google_maps_link = google_maps_link_generator(wedding_data.event.name_of_the_wedding_venue, wedding_data.event.wedding_venue_address)


    template_data = {
            "request": request,
            "church_google_maps_link": church_google_maps_link,
            "venue_google_maps_link": venue_google_maps_link,
            "wedding_date_iso": wedding_data.event.wedding_date_iso,
            "wedding_date_human": wedding_data.event.wedding_date_human,
            "wedding_date_time": wedding_data.event.wedding_date_time,
        }


    return templates.TemplateResponse(
        invitation_template,
        template_data
    )

