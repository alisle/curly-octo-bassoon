from __future__ import print_function

from googleapiclient.errors import HttpError
import spacy
import gdrive

from model import EntityType, DocumentType, Entity
from stream import Stream


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']


def main():
    stream = Stream()
    stream.create_stream(stream.stream_name)
    nlp = spacy.load("en_core_web_sm")
    
    creds = None
    creds = gdrive.Credentials()
    creds.authenticate()

    drive = gdrive.Drive(creds)
    doc = gdrive.Document(creds)

    files = drive.list()


    for file in files:
        print(u'{0}, {1}'.format(file['name'], file['id']))
        try:
            raw_text = doc.read(file['id'])
            processed_text = nlp(raw_text)

            
            
            orgs = set([entity.text for entity in processed_text.ents if entity.label_ == "ORG" ])
            persons = set([entity.text for entity in processed_text.ents if entity.label_ == "PERSON" ])

            for org in orgs: 
                entity = Entity(DocumentType.GDRIVE, file['id'], EntityType.ID, org)
                stream.post_entity(entity)
                

            for person in persons:
                entity = Entity(DocumentType.GDRIVE, file['id'], EntityType.ID, person)
                stream.post_entity(entity)


        except HttpError as error:
            print("Unable to process file")


if __name__ == '__main__':
    main()