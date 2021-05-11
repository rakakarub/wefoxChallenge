from kafka import KafkaConsumer
import os

class KafkaConsumerService:
    def __init__(self):
        self.consumer = KafkaConsumer(
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            bootstrap_servers = [os.getenv('KAFKA_HOST') + ':' + os.getenv('KAFKA_PORT')]
        )