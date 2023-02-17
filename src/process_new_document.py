from gremlin import GraphDB
from stream import KafkaStream, StreamName
from model import Document

import logging
from pprint import pprint


"""
{
  "document_details": {
    "document_type": "GDrive",
    "document_name": "Draft",
    "document_owners": [
      {
        "display_name": "ELLE TUPOU-LISLE",
        "email_address": "et91736@eanesisd.net"
      }
    ],
    "document_id": "1yGlYbgT-XeuAwwS2eesQgp00dLB2GFniwsdRWcoE2os",
    "shared": true,
    "shared_user": {
      "display_name": "ELLE TUPOU-LISLE",
      "email_address": "et91736@eanesisd.net"
    },
    "last_modifed": "2022-12-08T02:47:46.406Z"
  },
  "possible_company_keywords": [
    "Holden"
  ],
  "possible_human_keywords": [
    "Holden Caulfield",
    "Sally Hayes",
    "Zerby",
    "Holden",
    "Stradlater",
    "Ackley",
    "J.D. Salinger’s",
    "Holden Caufield",
    "Salinger",
    "Elle Tupou-Lisle",
    "J.D Salinger",
    "Sally"
  ],
  "entity_type": "document"
}
"""
def main():
    logging.basicConfig(level=logging.INFO)
    graph = GraphDB()
    stream = KafkaStream()

    logging.debug("creating consumer for document")
    consumer = stream.create_consumer(StreamName.NEW_DOCUMENT)
    
    with open("possible_names.txt", "a") as possible_names:                 
        for message in consumer:
            document = Document.from_json(message.value)            
            graph.insert(document.document_details)
            possible_names.write('\n'.join(document.possible_human_keywords) + '\n')     
            possible_names.flush()

               
        

if __name__ == '__main__':
    main()