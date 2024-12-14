from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from datetime import datetime
import os
import traceback

import webbrowser
webbrowser.register('windows-browser', None, webbrowser.BackgroundBrowser('/mnt/c/Program Files/Google/Chrome/Application/chrome.exe'))
webbrowser.get('windows-browser').open('https://www.google.com')


SCOPES = ['https://www.googleapis.com/auth/calendar']


def _get_account_credentials():
    try:
        SCOPES = ['https://www.googleapis.com/auth/calendar']
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'creds.json', SCOPES)
                creds = flow.run_local_server(port=8005)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        return creds
    except Exception as err:
        print(f"Error getting account credentials || {traceback.format_exc()}")
        raise err

def schedule_calendar_event(
    summary: str,
    description: str,
    attendee_emails: list,
    start_date_time: datetime,
    end_date_time: datetime
):
    try:
        creds = _get_account_credentials()
        service = build('calendar', 'v3', credentials=creds)
        event = {
            "summary": summary,
            "description": description,
            "start": {
                "dateTime": start_date_time.strftime("%Y-%m-%dT%H:%M:%S"),
                "timeZone": "Asia/Kolkata"
            },
            "end": {
                "dateTime": end_date_time.strftime("%Y-%m-%dT%H:%M:%S"),
                "timeZone": "Asia/Kolkata"
            },
            "attendees": [
                {"email": email} for email in attendee_emails
            ],
            "reminders": {
                "useDefault": False,
                "overrides": [
                    {"method": "email", "minutes": 24 * 60},
                    {"method": "popup", "minutes": 10},
                ],
            },
        }
        event = service.events().insert(calendarId='primary', body=event).execute()
        return event
    except Exception as err:
        print(f"Error scheduling calendar event || {traceback.format_exc()}")
        raise err
