from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

wedding_date_iso = '2026-07-26'
wedding_date_human = "26 lipca 2026 dupa"
wedding_date_time = '2026-07-26T16:30'
@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("invitation_base1.html", {"request": request,
                                                                "wedding_date_iso": wedding_date_iso,
                                                                "wedding_date_human": wedding_date_human,
                                                                "wedding_date_time": wedding_date_time})
