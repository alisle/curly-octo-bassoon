import json
from model import DocumentEntity, Human, DocumentDetails
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

    def post_entity(self, entity: DocumentEntity):
        logging.info(f"Posting Entity: {entity}")
        json_str : str = entity.to_json()
        self.put_record(StreamName.NEW_ENTITY, json_str)

