# GOOGLE LIBRARY
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None
# GOOGLE LIBRARY


class Calendar():
    def __init__(self, USER, LOCATION, SPORT, TIMESTART, TIMEEND, PEMAIN):
        self.USER = USER
        self.LOCATION = LOCATION
        self.SPORT = SPORT
        self.TIMESTART = TIMESTART
        self.TIMEEND = TIMEEND
        self.PEMAIN = PEMAIN


    def setCalendar(self):
        SCOPES = 'https://www.googleapis.com/auth/calendar'
        CLIENT_SECRET_FILE = 'client_secret.json'
        APPLICATION_NAME = 'Kick Off Buddies Calendar Reminder'
        cwd_dir = os.getcwd()
        credential_user = os.path.join(cwd_dir, '.credential')
        credential_dir = os.path.join(credential_user, str(self.USER))
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir, 'Calendar.json')

        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            return "No Creds"
            # flow = client.flow_from_clientsecrets(
            #     CLIENT_SECRET_FILE, SCOPES)
            # flow.user_agent = APPLICATION_NAME
            # if flags:
            #     credentials = tools.run_flow(flow, store, flags)
            # else:  # Needed only for compatibility with Python 2.6
            #     credentials = tools.run(flow, store)
            # print('Storing credentials to ' + credential_path)

        http = credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)
        acara = {
            'summary': self.SPORT,
            'location': self.LOCATION,
            'description': 'KickOffBuddies Reminder, verily sport makes you healthy and happy ',
            'start': {
                # 'dateTime': '2019-04-07T09:00:00-07:00',
                'dateTime': self.TIMESTART,
                'timeZone': 'America/Los_Angeles',
            },
            'end': {
                'dateTime': self.TIMEEND,
                'timeZone': 'America/Los_Angeles',
            },
            'recurrence': [
                'RRULE:FREQ=DAILY;COUNT=2'
            ],
            'attendees':[
            
            {'email': 'lpage@example.com'},
            {'email': 'sbrin@example.com'},
            ],
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                ],
            },
        }

        acara = service.events().insert(calendarId='primary', body=acara).execute()
        print('Event created: %s' % (acara.get('htmlLink')))
