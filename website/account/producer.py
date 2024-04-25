from kafka import KafkaProducer
from .utilities import kafka_producer_serializer


producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=kafka_producer_serializer)