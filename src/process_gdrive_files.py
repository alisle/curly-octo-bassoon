from __future__ import print_function

import logging
from googleapiclient.errors import HttpError
import spacy
import google_drive

from pprint import pprint
from model import EntityType, DocumentType, Entity
from stream import KafkaStream


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']


def main():
    logging.basicConfig(level=logging.INFO)

    stream = KafkaStream()
    nlp = spacy.load("en_core_web_sm")
    
    creds = None
    creds = google_drive.GoogleDriveCredentials()
    creds.authenticate()

    drive = google_drive.Drive(creds)
    drive_document_service = google_drive.Document(creds)

    documents = drive.list()
    

    
    logging.info("Processing Documents") 
    for doc in documents:
        try:                
            raw_text = drive_document_service.read(doc.document_id)            
            processed_text = nlp(raw_text)            
            
            orgs = set([entity.text for entity in processed_text.ents if entity.label_ == "ORG" ])
            persons = set([entity.text for entity in processed_text.ents if entity.label_ == "PERSON" ])

            for org in orgs: 
                entity = Entity(doc, EntityType.ID, org)
                stream.post_entity(entity)
                

            for person in persons:
                entity = Entity(doc, EntityType.ID, person)
                stream.post_entity(entity)


        except HttpError as error:
            logging.error("Unable to process file")


if __name__ == '__main__':
    main()