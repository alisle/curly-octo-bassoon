from stream import KafkaStream, StreamName
from pprint import pprint
import logging

def main():
    logging.basicConfig(level=logging.INFO)
    
    stream = KafkaStream()

    print("Creating Consumer")
    consumer = stream.create_consumer(StreamName.NEW_ENTITY)

    for message in consumer:
        print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
            message.offset, message.key,
            message.value))

if __name__ == '__main__':
    main()