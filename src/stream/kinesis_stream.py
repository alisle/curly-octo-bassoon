import boto
from boto.kinesis.exceptions import ResourceInUseException
import os
import uuid
from .stream_name import StreamName
from model import Entity

class KinesisStream:   
    new_entity_stream_name = "new_entity"
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

    def get_shard(self, stream_name : str) :
        r = self.kinesis.describe_stream(stream_name)
        description = r.get('StreamDescription')
        shards = description.get('Shards')
        return shards[0]['ShardId']


    def create_stream(self, stream_name : str):
        try:
            # create the stream
            self.kinesis.create_stream(stream_name, 1)
            logging.info('stream {} created in region {}'.format(stream_name, self.region))
        except ResourceInUseException:
            logging.info('stream {} already exists in region {}'.format(stream_name, self.region))
    

    def put_record(self, stream_name : StreamName, data : str):
        if self.get_status(stream_name) == "ACTIVE":
            """put a single record to the stream"""
            response = self.kinesis.put_record(stream_name, data, self.partition_key)
        else:
            logging.error(f"Unable to post to kinesis {self.get_status()}")
        

    def post_entity(self, entity: Entity):
        logging.info(f"ENTITY POSTING: {entity}")
        json_str : str = entity.to_json()
        self.put_record(StreamName.NEW_ENTITY, json_str)

    def get_record(self, stream_name : StreamName, data : str):
        if self.get_status(stream_name) == "ACTIVE":
            self.kinesis.get_record(stream_name)

        self.kinesis.get_shard

    def create_iterator(self, stream_name : str):
        shard = self.get_shard(stream_name)
        logging.info(f"Creating iterator for stream {stream_name}:{shard}")

        response = self.kinesis.get_shard_iterator(
            stream_name=stream_name,
            shard_id=shard,
            shard_iterator_type='TRIM_HORIZON'
        )
        return response.get('ShardIterator')


    def get_next_records(self,  shard_iterator, num_of_records : int):
        response = self.kinesis.get_records( shard_iterator=shard_iterator, limit= num_of_records)
        shard_iterator = response.get("NextShardIterator")
        records = response.get("Records")

        return shard_iterator, records

