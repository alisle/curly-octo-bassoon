from stream import KafkaStream, StreamName
from pprint import pprint
from model import Human, APIHuman, APIType, APIDetails
import logging
from pprint import pprint
from gremlin import GraphDB
import random
import string


def main():
    logging.basicConfig(level=logging.INFO)        
    logging.debug("creating graph")
    graph = GraphDB()   
    stream = KafkaStream()

    logging.debug("creating consumer for api_human")
    consumer = stream.create_consumer(StreamName.NEW_API_HUMAN)

    for message in consumer:        
        logging.info("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
            message.offset, message.key,
            message.value))
            
        entity = APIHuman.from_json(message.value)
        graph.insert(entity)


if __name__ == '__main__':
    main()