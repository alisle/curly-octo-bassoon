import os.path

from google.oauth2.credentials import Credentials as GoogleCredentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from model import DocumentDetails, DocumentUser
from typing import List
from pprint import pprint

import logging

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
        

"""
Example of a full set of fields from google drive
{'capabilities': {'canAcceptOwnership': False,
                  'canAddChildren': False,
                  'canAddMyDriveParent': False,
                  'canChangeCopyRequiresWriterPermission': False,
                  'canChangeSecurityUpdateEnabled': False,
                  'canChangeViewersCanCopyContent': False,
                  'canComment': True,
                  'canCopy': True,
                  'canDelete': False,
                  'canDownload': True,
                  'canEdit': True,
                  'canListChildren': False,
                  'canModifyContent': True,
                  'canModifyLabels': False,
                  'canMoveChildrenWithinDrive': False,
                  'canMoveItemIntoTeamDrive': False,
                  'canMoveItemOutOfDrive': False,
                  'canMoveItemWithinDrive': True,
                  'canReadLabels': False,
                  'canReadRevisions': True,
                  'canRemoveChildren': False,
                  'canRemoveMyDriveParent': True,
                  'canRename': True,
                  'canShare': True,
                  'canTrash': False,
                  'canUntrash': False},
 'copyRequiresWriterPermission': False,
 'createdTime': '2022-11-14T04:05:42.960Z',
 'explicitlyTrashed': False,
 'hasThumbnail': True,
 'iconLink': 'https://drive-thirdparty.googleusercontent.com/16/type/application/vnd.google-apps.document',
 'id': '1yGlYbgT-XeuAwwS2eesQgp00dLB2GFniwsdRWcoE2os',
 'isAppAuthorized': False,
 'kind': 'drive#file',
 'lastModifyingUser': {'displayName': 'ELLE TUPOU-LISLE',
                       'emailAddress': 'et91736@eanesisd.net',
                       'kind': 'drive#user',
                       'me': False,
                       'permissionId': '15494378695015086929',
                       'photoLink': 'https://lh3.googleusercontent.com/a-/AD5-WCmtlGm5G1n2rAdQ_pyTLTmDEkUqUC1-u1dXwe4sqw=s64'},
 'linkShareMetadata': {'securityUpdateEligible': False,
                       'securityUpdateEnabled': True},
 'mimeType': 'application/vnd.google-apps.document',
 'modifiedByMe': True,
 'modifiedByMeTime': '2022-11-16T03:13:30.805Z',
 'modifiedTime': '2022-12-08T02:47:46.406Z',
 'name': 'Draft',
 'ownedByMe': False,
 'owners': [{'displayName': 'ELLE TUPOU-LISLE',
             'emailAddress': 'et91736@eanesisd.net',
             'kind': 'drive#user',
             'me': False,
             'permissionId': '15494378695015086929',
             'photoLink': 'https://lh3.googleusercontent.com/a-/AD5-WCmtlGm5G1n2rAdQ_pyTLTmDEkUqUC1-u1dXwe4sqw=s64'}],
 'permissionIds': ['15830344643349030892', '15494378695015086929'],
 'permissions': [{'deleted': False,
                  'displayName': 'Alex Lisle',
                  'emailAddress': 'alex.lisle@gmail.com',
                  'id': '15830344643349030892',
                  'kind': 'drive#permission',
                  'pendingOwner': False,
                  'photoLink': 'https://lh3.googleusercontent.com/a/AEdFTp7Dx-HHELmtEjbI8hsd6EZDuBGXARofzqH1X5ke=s64',
                  'role': 'writer',
                  'type': 'user'},
                 {'deleted': False,
                  'displayName': 'ELLE TUPOU-LISLE',
                  'emailAddress': 'et91736@eanesisd.net',
                  'id': '15494378695015086929',
                  'kind': 'drive#permission',
                  'pendingOwner': False,
                  'photoLink': 'https://lh3.googleusercontent.com/a-/AD5-WCmtlGm5G1n2rAdQ_pyTLTmDEkUqUC1-u1dXwe4sqw=s64',
                  'role': 'owner',
                  'type': 'user'}],
 'quotaBytesUsed': '3657',
 'shared': True,
 'sharedWithMeTime': '2022-11-16T03:02:18.443Z',
 'sharingUser': {'displayName': 'ELLE TUPOU-LISLE',
                 'emailAddress': 'et91736@eanesisd.net',
                 'kind': 'drive#user',
                 'me': False,
                 'permissionId': '15494378695015086929',
                 'photoLink': 'https://lh3.googleusercontent.com/a-/AD5-WCmtlGm5G1n2rAdQ_pyTLTmDEkUqUC1-u1dXwe4sqw=s64'},
 'size': '3657',
 'spaces': ['drive'],
 'starred': False,
 'thumbnailVersion': '46',
 'trashed': False,
 'version': '121',
 'viewedByMe': True,
 'viewedByMeTime': '2022-11-16T03:13:30.805Z',
 'viewersCanCopyContent': True,
 'webViewLink': 'https://docs.google.com/document/d/1yGlYbgT-XeuAwwS2eesQgp00dLB2GFniwsdRWcoE2os/edit?usp=drivesdk',
 'writersCanShare': True}
"""

class Drive:
    def __init__(self, credentials = None) -> None:
        if credentials is None:
            credentials = Credentials()

        self.__credentials = credentials

    def __create_user(self, user : dict) -> DocumentUser:
        return DocumentUser(user['displayName'], user['emailAddress'])

    def __create_users(self, users: List[dict]) -> List[DocumentUser]:
        return [self.__create_user(user) for user in users]

    def __process_files(self, files) -> List[DocumentDetails]:
        documents = []
        for file in files:
            logging.info("Processing new file")

            owners = self.__create_users(file['owners']) 
            id = file['id']
            modified_time = file['modifiedTime']
            name = file['name']
            shared = file['shared']
            sharing_user = None

            if "sharingUser" in file:
                sharing_user = self.__create_user(file['sharingUser'])

            doc = DocumentDetails(name, owners, id, shared, sharing_user, modified_time) 

            documents.append(doc)
        

        return documents


    def list(self) -> List[DocumentDetails]:
        files = []
        if not self.__credentials.authenticated():
            self.__credentials.authenticate()

        try:
            service = build("drive", "v3", credentials=self.__credentials.get())
            token = None
            
            while True:
                results = service.files().list(
                    pageSize=1000, pageToken=token, fields="nextPageToken, files(id, name, owners, shared, sharingUser, modifiedTime)").execute()
                
                token = results.get('nextPageToken', None)
                items = results.get('files', [])
                files = files + items

                if not items or not token:                    
                    return self.__process_files(files)


            
        except HttpError as error:
            logging.ERROR(f'An error occurred: {error}')
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



    