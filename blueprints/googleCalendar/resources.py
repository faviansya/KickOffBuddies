from __future__ import print_function
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

import auth
class Calendar():
    def __init__(self,sport,location,timestart,timeend,player):
        self.sport = sport
        self.location = location
        self.timestart = timestart
        self.timeend = timeend
        self.player = player

    def commitCalendars(self):
        data=input("Masukkan Data:")
        data = str(data)
        SCOPES = 'https://www.googleapis.com/auth/calendar'
        CLIENT_SECRET_FILE = 'client_secret.json'
        APPLICATION_NAME = 'Kick Off Buddies Calendar'
        print("masokkk")
        authInst = auth.auth(SCOPES,CLIENT_SECRET_FILE,APPLICATION_NAME,data)
        credentials = authInst.get_credentials()

        http = credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)

        # event = {
        #     'summary': self.sport,
        #     'location': self.location,
        #     'description': 'Notification From Kick Off Buddies, Sport Is Life Sport Is Love',
        #     'start': {
        #         # 'dateTime': '2019-04-07T09:00:00-07:00',
        #         'dateTime': self.timestart,
        #         'timeZone': 'Indonesia/Malang',
        #     },
        #     'end': {
        #         'dateTime': self.timeend,
        #         'timeZone': 'Indonesia/Malang',
        #     },
        #     'recurrence': [
        #         'RRULE:FREQ=DAILY;COUNT=2'
        #     ],
        #     'attendees': self.player
        #         # {'email': 'lpage@example.com'},
        #         # {'email': 'sbrin@example.com'},
        #     ,
        #     'reminders': {
        #         'useDefault': False,
        #         'overrides': [
        #         {'method': 'email', 'minutes': 24 * 60},
        #         {'method': 'popup', 'minutes': 10},
        #         ],
        #     },
        # }

        # event = service.events().insert(calendarId='primary', body=event).execute()
        # print ('Event created: %s' % (event.get('htmlLink')))