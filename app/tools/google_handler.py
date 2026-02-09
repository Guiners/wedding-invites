import os
from urllib.parse import quote_plus

import yagmail
from dotenv import load_dotenv

load_dotenv()


def send_email(client_email: str, subject: str, message: str):
    yag = yagmail.SMTP(os.getenv("EMAIL_LOGIN"), os.getenv("EMAIL_PASSWORD"))
    yag.send(to=client_email, subject=subject, contents=message)


nazwa_kosciola = "Parafia Rzymskokatolicka św. Józefa"
adres_kosciola = "Lublin"

nazwa_lokalu_weselnego = "Karczma Bida"
adres_lokalu_weselnego = "Bogucin"


def google_maps_link_generator(address: str, name: str):
    return (
        f"https://www.google.com/maps/search/?api=1&query={quote_plus(address + name)}"
    )
