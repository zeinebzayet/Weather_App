from kafka import KafkaConsumer
from pymongo import MongoClient
import json

# Set up Kafka consumer
consumer = KafkaConsumer('weather_topic',
                             bootstrap_servers=['kafka:9092'],
                             auto_offset_reset='earliest',
                             group_id='my-group',
                             value_deserializer=lambda x: json.loads(x.decode('utf-8')),
                             api_version=(0, 10, 0))


# Set up MongoDB client and database
client = MongoClient('mongodb://172.18.0.7:27017/',username='admin',
                 password='password')


db = client['weatherdatabase']

# Set up MongoDB collection
collection = db['weathercollection']


for message in consumer:
    # Insert data into MongoDB
    collection.insert_one(message.value)
