EXCEL_SHEET_NAMES_MAP = {
    "invitation_sheet": "Informacje o Zaproszeniu",
    "event_sheet": "Informacje o Wydarzeniu",
    "guests_sheet": "Lista Gości",
}


GUESTS_COL_MAP = {
    "Osoby zaproszone": "invited_guests",
    "Zaproszenie specjalne": "special_invitation",
    "Z osobą towarzyszącą?": "with_plus_one",
    "Z dziećmi?": "with_children",
    "Z noclegiem?": "with_accommodation",
}

INVITATION_COL_MAP = {
    "Model zaproszenia": "invitation_model",
    "Dodatkowa kartka": "additional_card",
    "Kolor koperty": "envelope_color",
    "Personalizacja koperty": "envelope_personalization",
    "Lack Koperty": "envelope_wax_seal",
    "Wstążka na kopercie": "envelope_ribbon",
    "Złocenie Koperty": "envelope_foil_stamping",
    "Link do piosenki (jeśli obowiązuje)": "song_link",
}

EVENT_COL_MAP = {
    "lmię Pani Młodej": "brides_first_name",
    "Nazwisko Pani Młodej": "brides_last_name",
    "Telefon do Pani Młodej": "brides_phone_number",
    "lmię Pana Młodego": "grooms_first_name",
    "Nazwisko Pana Młodego": "grooms_last_name",
    "Telefon do Pana Młodego": "grooms_phone_number",
    "Data ślubu": "wedding_date",
    "Godzina ślubu": "wedding_time",
    "Do kiedy potwierdzić obecność RSVP (data)": "rsvp_deadline_date",
    "Nazwa Kościoła": "name_of_the_church",
    "Adres Kościoła": "church_address",
    "Nazwa Lokalu Weselnego": "name_of_the_wedding_venue",
    "Adres Lokalu Weselnego": "wedding_venue_address",
    "Kwiaty czy Alkohol? A może coś inego?": "flowers_or_alcohol",
    "Prezenty czy koperty? A może coś innego?": "gifts_or_cash",
    "Czy na wesele będą zapraszane dzieci?": "children_be_invited",
}

PL_MAP = str.maketrans("ąćęłńóśżźĄĆĘŁŃÓŚŻŹ", "acelnoszzACELNOSZZ")
