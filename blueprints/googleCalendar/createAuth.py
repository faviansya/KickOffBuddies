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

SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Kick Off Buddies Calendar'
authInst = auth.auth(SCOPES,CLIENT_SECRET_FILE,APPLICATION_NAME,"Faviansyah1")
credentials = authInst.get_credentials()

http = credentials.authorize(httplib2.Http())
service = discovery.build('calendar', 'v3', http=http)
