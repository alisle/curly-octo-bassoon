from __future__ import print_function
from stream import Stream
import time
from pprint import pprint


def main():
    stream = Stream()

    iterator = stream.create_iterator(stream.new_entity_stream_name)
    iterator, records = stream.get_next_records(iterator, 10)

    has_records = True
    while True:
        iterator, records = stream.get_next_records(iterator, 10)
        if len(records) == 0:
            has_records = False

        print(f"Got Records {len(records)}")
        pprint(records)

        time.sleep(1)


if __name__=='__main__':
    main()