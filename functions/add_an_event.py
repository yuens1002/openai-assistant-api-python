from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import pickle
import os.path
from datetime import datetime

# Get the directory of the current file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Get the path to the parent directory
parent_dir = os.path.dirname(current_dir)

# Construct the path to 'credentials.json' in the parent directory
credentials_path = os.path.join(parent_dir, "credentials.json")
# Construct the path to 'token.pickle' in the parent directory
pickle_token_path = os.path.join(parent_dir, "token.pickle")

# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ["https://www.googleapis.com/auth/calendar"]


def authenticate_google_calendar():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens.
    if os.path.exists(pickle_token_path):
        with open(pickle_token_path, "rb") as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(pickle_token_path, "wb") as token:
            pickle.dump(creds, token)
    return creds


def to_iso_time(date_time_str):
    return datetime.strptime(date_time_str, "%m/%d/%Y %I:%M %p").isoformat()


def create_event(start_date_time, end_date_time, **kwargs):
    creds = authenticate_google_calendar()
    service = build("calendar", "v3", credentials=creds)

    event = {
        "summary": kwargs.get("event_name"),
        "location": kwargs.get("location"),
        "description": kwargs.get("description"),
        "start": {
            "dateTime": to_iso_time(start_date_time),
            "timeZone": "America/New_York",
        },
        "end": {
            "dateTime": to_iso_time(end_date_time),
            "timeZone": "America/New_York",
        },
        "attendees": kwargs.get("attendees"),
        "reminders": {
            "useDefault": kwargs.get("reminder_default"),
            "overrides": kwargs.get("reminders"),
        },
    }

    return service.events().insert(calendarId="primary", body=event).execute()
