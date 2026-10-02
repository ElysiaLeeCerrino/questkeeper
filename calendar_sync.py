import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/calendar"]
CALENDAR_ID = os.getenv("GOOGLE_CALENDAR_ID")

def get_calendar_service():
    """
    Supports two ways to provide credentials:
    1. GOOGLE_CREDENTIALS_JSON  – full JSON content as a string (best for Render)
    2. GOOGLE_CREDENTIALS       – path to a service-account.json file (local use)
    """
    json_str = os.getenv("GOOGLE_CREDENTIALS_JSON")
    if json_str:
        info = json.loads(json_str)
        creds = service_account.Credentials.from_service_account_info(info, scopes=SCOPES)
    else:
        credentials_file = os.getenv("GOOGLE_CREDENTIALS", "./service-account.json")
        creds = service_account.Credentials.from_service_account_file(
            credentials_file, scopes=SCOPES
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
