from datetime import datetime
import traceback

import aiohttp
from app.models.user import User

    
async def schedule_calendar_event_async(
    user : User,
    summary: str,
    description: str,
    attendee_emails: list,
    start_date_time: datetime,
    end_date_time: datetime
):
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
    
    events_api = "https://www.googleapis.com/calendar/v3/calendars/primary/events"
    try:
        calendar_access_token = user.google_calendar_access_token
        headers = {
            "Authorization": f"Bearer {calendar_access_token}"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(events_api, headers=headers, json=event) as response:
                if response.status == 200:
                    response_dict = await response.json()
                else:
                    raise Exception(f"{response.status} || {response.text}")
                return response_dict
    except Exception as err:
        print(f"Error scheduling calendar event || {traceback.format_exc()}")
        raise err