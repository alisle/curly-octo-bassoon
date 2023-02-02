import json
from model import Entity
from kafka import KafkaProducer, KafkaConsumer
from .stream_name import StreamName
import logging 
import os


class KafkaStream:
    def __init__(self) -> None:
        if os.getenv('KAFKA_SERVER') is not None:
            self.server = os.getenv('KAFKA_SERVER')
        else:
            self.server = 'localhost:19092'

        logging.debug(f"Setting Kafka server to {self.server}")

        self.producer = KafkaProducer(bootstrap_servers=[self.server])

    def create_consumer(self, stream_name : StreamName):
        return KafkaConsumer(stream_name.value, bootstrap_servers=[self.server])

    def __put_record(self, stream_name : StreamName, data: str):
        self.producer.send(stream_name.value, data.encode('utf-8'))


    def flush(self):
        self.producer.flush()

    def post(self, stream_name : StreamName, entity: Entity):
        if not issubclass(Entity, entity.__class__):
            logging.ERROR("Unable to post as this isn't an entity")
            return
        
        logging.info(f"Posting Entity: {entity.entity_type}")
        json_str : str = entity.to_json()
        self.__put_record(stream_name, json_str)
        

