from __future__ import print_function
from stream import Stream


def main():
    stream = Stream()
    iterator = stream.create_iterator(stream.stream_name)

    has_records = True
    while(has_records):
        iterator, records = stream.get_next_records(iterator, 10)
        if len(records) == 0:
            has_records = False

        print(f"Got Records {len(records)}")
        print(records)


if __name__=='__main__':
    main()