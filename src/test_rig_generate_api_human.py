from stream import KafkaStream, StreamName
from model import Human, APIHuman, APIType, APIDetails
from test_rig_utils import create_name_email, get_api_name


import logging
from pprint import pprint

def main():
    logging.basicConfig(level=logging.DEBUG)
    stream = KafkaStream()

    n = 0
    while n < 100:
        details = create_name_email()
        pprint(details)

        human  = Human(details['display_name'], details['email_address'])
        api = get_api_name()

        api_human = APIHuman(APIDetails(api), human)
        stream.post(StreamName.NEW_API_HUMAN, api_human)

        n += 1

    

if __name__ == '__main__':
    main()