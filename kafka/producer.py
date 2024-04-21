from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='localhost:9092')
producer.send('test', b'fuck, Kafka!')
producer.flush()
producer.close()