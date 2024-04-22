from kafka import KafkaConsumer
import json

consumer = KafkaConsumer('copy-trade', bootstrap_servers='localhost:9092')

for message in consumer:
    print(json.loads(message.value))