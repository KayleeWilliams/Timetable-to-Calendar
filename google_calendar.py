import os.path
import time
import functools
from multiprocessing import Pool
from venv import create
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/calendar']

# Loop through all events, if they match with the inputted event, delete it.
def remove_event(service, id, data):
    page_token = None
    while True:
        events = service.events().list(calendarId=id, pageToken=page_token).execute()
        for event in events['items']:
            if ((data[0] in event['start']['dateTime']) and (data[1] in event['end']['dateTime'])):
                service.events().delete(
                    calendarId=id, eventId=event['id']).execute()
        page_token = events.get('nextPageToken')
        if not page_token:
            break

# Create an event.
def create_event(service, id, data):
    event = {
        'summary': data[2],
        'location': data[4],
        'description': data[3],
        'start': {
            'dateTime': data[0],
            'timeZone': 'Europe/London',
        },
        'end': {
            'dateTime': data[1],
            'timeZone': 'Europe/London',
        },
    }
    event = service.events().insert(calendarId=id, body=event).execute()


def main(new_events, removed_events):
    # token.json -> Stores user's access and refresh tokens
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If Credentials invallid, log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        # Check if a university calendar exists
        calendar_list = service.calendarList().list().execute()
        found = False
        id = None
        for calendar in calendar_list['items']:
            if calendar['summary'] == 'University':
                id = calendar['id']
                found = True
                break

        # If it doesnt exist, create one
        if found == False:
            calendar = {
                'summary': 'University',
                'timeZone': 'Europe/London'
            }

            created_calendar = service.calendars().insert(body=calendar).execute()
            id = created_calendar['id']
            time.sleep(3)

        # Using multiprocessing to remove/add events. 
        if len(removed_events) > 0:
            with Pool() as p:
                p.map(functools.partial(remove_event, service, id), removed_events)

        if len(new_events) > 0:
            with Pool() as p:
                p.map(functools.partial(create_event, service, id), new_events)

    except HttpError as error:
        print('An error occurred:', error)


if __name__ == "__main__":
    main()
