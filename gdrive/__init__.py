import os.path

from google.oauth2.credentials import Credentials as GoogleCredentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class Credentials:
    SCOPES = [
        'https://www.googleapis.com/auth/documents.readonly',
        'https://www.googleapis.com/auth/drive.metadata.readonly'
        ]

    __creds = None
    

    def __init__(self) -> None:
        pass

    def authenticate(self):
        self.__creds = None

        if os.path.exists('token.json'):
            self.__creds = GoogleCredentials.from_authorized_user_file('token.json', self.SCOPES)

        # If there are no (valid) credentials available, let the user log in.
        if not self.__creds or not self.__creds.valid:
            if self.__creds and self.__creds.expired and self.__creds.refresh_token:
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
        


class Drive:
    def __init__(self, credentials = None) -> None:
        if credentials is None:
            credentials = Credentials()

        self.__credentials = credentials

    def list(self):
        files = []
        if not self.__credentials.authenticated():
            self.__credentials.authenticate()

        try:
            service = build("drive", "v3", credentials=self.__credentials.get())
            token = None
            
            while True:
                print("Loop")
                results = service.files().list(
                    pageSize=1000, pageToken=token, fields="nextPageToken, files(id, name)").execute()
                
                token = results.get('nextPageToken', None)
                items = results.get('files', [])
                files = files + items

                if not items or not token:                    
                    return files


            
        except HttpError as error:
            print(f'An error occurred: {error}')
            return None

class Document:
    def __init__(self, credentials = None) -> None:
        if credentials is None:
            credentials = Credentials()
        
        self.__credentials = credentials
        self.__service = build("docs", "v1", credentials=self.__credentials.get())


    def parse_paragraph(self, element):
        text_run = element.get('textRun')
        if not text_run:
            return ''

        return text_run.get('content')

    def parse_elements(self, elements):
        text = ''
        for value in elements:
            if 'paragraph' in value:
                elements = value.get('paragraph').get('elements')
                for element in elements:
                    text += self.parse_paragraph(element)
            elif 'table' in value:
                table = value.get('table')
                for row in table.get('tableRows'):
                    cells = row.get('tableCells')
                    for cell in cells:
                        text += self.parse_elements(cell.get('content'))
            elif 'tableOfContents' in value:
                toc = value.get('tableOfContents')
                text += self.parse_elements(toc.get('content'))
        return text

    def read(self, documentID):
        doc = self.__service.documents().get(documentId=documentID).execute()
        contents = doc.get('body').get('content')
        return self.parse_elements(contents)



    