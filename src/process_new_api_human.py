from stream import KafkaStream, StreamName
from pprint import pprint
from model import Human, APIHuman, APIType, APIDetails
import logging
from pprint import pprint
from gremlin import GraphDB
import random
import string


def main():
    logging.basicConfig(level=logging.DEBUG)    
    logging.debug("creating graph")
    graph = GraphDB()   

    logging.debug("looping through entities")
    n = 0
    while n < 25:
        logging.debug("creating entity")
        entity = Human(''.join(random.choices(string.ascii_lowercase, k=5)), ''.join(random.choices(string.ascii_lowercase, k=10)))
        logging.debug("inserting entity")
        graph.insert(APIHuman(APIDetails(APIType.GOOGLE), entity))
        n += 1


"""
    #stream = KafkaStream()
    graph = GraphDB()


    graph.insert_api_type(APIType.GOOGLE)

    graph.insert_api_type(APIType.HUBSPOT)

    while True:
        entity = Human("Tina Lisle", "tina.lisle@gmail.com")

        pprint(entity)
        graph.insert_human(entity)
        graph.insert_api_human(APIHuman(APIDetails(APIType.GOOGLE), entity))

        entity = Human("Helena Lisle", "helena.lisle@gmail.com")
        graph.insert_human(entity)
        graph.insert_api_human(APIHuman(APIDetails(APIType.GOOGLE), entity))

        entity = Human("Penelope Lisle", "Penelope.lisle@gmail.com")
        graph.insert_human(entity)
        graph.insert_api_human(APIHuman(APIDetails(APIType.GOOGLE), entity))

        entity = Human("Elle Lisle", "elle.lisle@gmail.com")
        graph.insert_human(entity)
        graph.insert_api_human(APIHuman(APIDetails(APIType.GOOGLE), entity))
"""
"""
    logging.debug("creating new user consumer")
    consumer = stream.create_consumer(StreamName.NEW_API_HUMAN)

    for message in consumer:
        logging.info("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
            message.offset, message.key,
            message.value))
        
        entity = APIHuman.from_json(message.value)
        pprint(entity.human.display_name)
        pprint(entity.human.email_address)

"""
        


if __name__ == '__main__':
    main()