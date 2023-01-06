from google.oauth2.credentials import Credentials as GoogleCredentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
import logging


class GoogleDriveCredentials:
    SCOPES = [
        'https://www.googleapis.com/auth/documents.readonly',
        'https://www.googleapis.com/auth/drive.metadata.readonly'
        ]

    __creds = None


    def authenticate(self):
        self.__creds = None

        if os.path.exists('token.json'):
            self.__creds = GoogleCredentials.from_authorized_user_file('token.json', self.SCOPES)
        else:
            logging.info('token.json does not exist, creating them')

        # If there are no (valid) credentials available, let the user log in.
        if not self.__creds or not self.__creds.valid:
            if self.__creds and self.__creds.expired and self.__creds.refresh_token:                
                logging.error("we need to refresh our request")
                self.__creds.refresh(Request())
            else:                
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                self.__creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(self.__creds.to_json())
        
        return True

    def get(self):
        return self.__creds

    def authenticated(self):
        return self.__creds is not None