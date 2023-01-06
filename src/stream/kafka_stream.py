import json
from model import DocumentEntity, Human, DocumentDetails, APIEntity, APIHumanEntity
from kafka import KafkaProducer, KafkaConsumer
from .stream_name import StreamName
import logging 



class KafkaStream:
    server = 'localhost:19092'

    producer = KafkaProducer(bootstrap_servers=[server])

    def create_consumer(self, stream_name : StreamName):
        return KafkaConsumer(stream_name.value, bootstrap_servers=[self.server])

    def put_record(self, stream_name : StreamName, data: str):
        self.producer.send(stream_name.value, data.encode('utf-8'))


    def flush(self):
        self.producer.flush()

    def post_document_entity(self, entity: DocumentEntity):
        logging.info(f"Posting Document Entity: {entity}")
        json_str : str = entity.to_json()
        self.put_record(StreamName.NEW_ENTITY, json_str)
    
    def post_api_entity(self, entity: APIEntity):
        logging.info(f"Posting API Entity {entity}")
        json_str : str = entity.to_json()
        self.put_record(StreamName.NEW_API_ENTIY, json_str)

    def post_api_human_entity(self, entity: APIHumanEntity):
        logging.info(f"POST API Human {entity}")
        json_str : str = entity.to_json()
        self.put_record(StreamName.NEW_API_HUMAN, json_str)
        

