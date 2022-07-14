from __future__ import print_function
import os
import uu
import boto
from boto.kinesis.exceptions import ResourceInUseException

from enum import Enum

from numpy import partition
from model import Entity

import uuid

class StreamName(str, Enum):
    NEW_ENTITY : str = "new_entity"

class Stream:   
    stream_name = "new_entity"
    region = 'us-east-1'
    aws_profile = 'kinesis-entity-consumer' 
    partition_key = str(uuid.uuid1())
    kinesis = None


    def __init__(self) -> None:
        os.environ['AWS_PROFILE'] = self.aws_profile
        self.kinesis = boto.kinesis.connect_to_region(self.region)



    def get_status(self, stream_name : str):
        r = self.kinesis.describe_stream(stream_name)
        description = r.get('StreamDescription')
        status = description.get('StreamStatus')
        return status

    def create_stream(self, stream_name : str):
        try:
            # create the stream
            self.kinesis.create_stream(stream_name, 1)
            print('stream {} created in region {}'.format(stream_name, self.region))
        except ResourceInUseException:
            print('stream {} already exists in region {}'.format(stream_name, self.region))
    

    def put_record(self, stream_name : StreamName, data : str):
        if self.get_status(stream_name) == "ACTIVE":
            """put a single record to the stream"""
            self.kinesis.put_record(stream_name, data, self.partition_key)
        else:
            print(f"Unable to post to kinesis {self.get_status()}")
        

    def post_entity(self, entity: Entity):
        print(f"ENTITY POSTING: {entity}")
        json_str : str = entity.to_json()
        self.put_record(StreamName.NEW_ENTITY, json_str)
