import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/calendar"]
CREDENTIALS_FILE = os.getenv("GOOGLE_CREDENTIALS")
CALENDAR_ID = os.getenv("GOOGLE_CALENDAR_ID")

def get_calendar_service():
    creds = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE, scopes=SCOPES
    )
    return build("calendar", "v3", credentials=creds)

def create_event(title, description, start_iso, end_iso=None):
    service = get_calendar_service()
    event = {
        "summary": title,
        "description": description or "",
        "start": {
            "dateTime": start_iso,
            "timeZone": "Europe/London"
        },
        "end": {
            "dateTime": end_iso or start_iso,
            "timeZone": "Europe/London"
        },
    }
    created = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
    return created.get("id")

def update_event(event_id, title=None, description=None, start_iso=None, end_iso=None):
    service = get_calendar_service()
    event = service.events().get(calendarId=CALENDAR_ID, eventId=event_id).execute()

    if title:
        event["summary"] = title
    if description is not None:
        event["description"] = description
    if start_iso:
        event["start"] = {"dateTime": start_iso, "timeZone": "Europe/London"}
    if end_iso:
        event["end"] = {"dateTime": end_iso, "timeZone": "Europe/London"}

    service.events().update(
        calendarId=CALENDAR_ID, eventId=event_id, body=event
    ).execute()
