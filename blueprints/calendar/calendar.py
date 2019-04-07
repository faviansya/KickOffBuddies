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
import threading
import time
import queue

class Calendar():
    def __init__(self,event,USER):
        self.event = event
        self.USER = USER

    def flags(self):
        time.sleep(1)
        self.event.set()
        print("Waiting For Auth")
        time.sleep(5)
        self.event.clear()

    def setCalendar(self):
        self.event.wait()
        if (self.event.is_set()):
            SCOPES = 'https://www.googleapis.com/auth/calendar'
            CLIENT_SECRET_FILE = 'client_secret.json'
            APPLICATION_NAME = 'Kick Off Buddies Calendar'
            cwd_dir = os.getcwd()
            credential_user = os.path.join(cwd_dir, '.credential')
            credential_dir = os.path.join(credential_user, str(self.USER))
            if not os.path.exists(credential_dir):
                os.makedirs(credential_dir)
            credential_path = os.path.join(credential_dir, 'Calendar.json')

            store = Storage(credential_path)
            credentials = store.get()
            if not credentials or credentials.invalid:
                flow = client.flow_from_clientsecrets(
                    CLIENT_SECRET_FILE, SCOPES)
                flow.user_agent = APPLICATION_NAME
                if flags:
                    credentials = tools.run_flow(flow, store, flags)
                else:  # Needed only for compatibility with Python 2.6
                    credentials = tools.run(flow, store)
                print('Storing credentials to ' + credential_path)
            time.sleep(1)
