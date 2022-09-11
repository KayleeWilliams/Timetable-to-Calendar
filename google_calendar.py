import os.path
import csv 
import time

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/calendar']

def main():
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

        # Clear the university calender in preperation of adding newer data 
        # https://developers.google.com/calendar/api/v3/reference/events/list
        page_token = None
        while True:
            events = service.events().list(calendarId=id, pageToken=page_token).execute()
            for event in events['items']:
                service.events().delete(calendarId=id, eventId=event['id']).execute()
            page_token = events.get('nextPageToken')
            if not page_token:
                break
        
        # Make a new event for each row
        with open('schedule.csv', 'r') as file:
            f = csv.reader(file)

            for row in f:
                event = {
                    'summary': row[2],
                    'location': row[4],
                    'description': row[3],
                    'start': {
                        'dateTime': row[0],
                        'timeZone': 'Europe/London',
                    },
                    'end': {
                        'dateTime': row[1],
                        'timeZone': 'Europe/London',
                    },
                    }
                
                event = service.events().insert(calendarId=id, body=event).execute()

    except HttpError as error:
        print('An error occurred:', error)
