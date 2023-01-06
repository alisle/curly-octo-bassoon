from stream import KafkaStream, StreamName
from pprint import pprint
from model import Human
import logging
from pprint import pprint

def main():
    logging.basicConfig(level=logging.INFO)
    
    stream = KafkaStream()

    logging.debug("creating new user consumer")
    consumer = stream.create_consumer(StreamName.NEW_USER)

    for message in consumer:
        logging.info("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
            message.offset, message.key,
            message.value))
        
        user = Human.from_json(message.value)
        pprint(user.display_name)
        pprint(user.email_address)

if __name__ == '__main__':
    main()