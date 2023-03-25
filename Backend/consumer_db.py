from kafka import KafkaConsumer
from pymongo import MongoClient
import json
import datetime



def extract_weather_data():

    # Set up Kafka consumer
    
    consumer = KafkaConsumer('weather_topic',
                             bootstrap_servers=['kafka:9092'],
                             auto_offset_reset='earliest',
                             group_id=None,
                             value_deserializer=lambda x: json.loads(x.decode('utf-8')),
                             consumer_timeout_ms=1000,
                             api_version=(0, 10, 0))
   

        

    for message in consumer:
        message_dict = json.loads(json.dumps(message.value))

        # message value and key are raw bytes -- decode if necessary!
        # e.g., for unicode: message.value.decode('utf-8')
        lon =  message_dict['coord']['lon']
        lat =  message_dict['coord']['lat']
        description =  message_dict['weather'][0]['description']
        temp = message_dict['main']['temp']
        temp_min =  message_dict['main']['temp_min']
        temp_max = message_dict['main']['temp_max']
        pressure =  message_dict['main']['pressure']
        humidity = message_dict['main']['humidity']
        visibility =  message_dict['visibility']
        speed =  message_dict['wind']['speed']
        deg =  message_dict['wind']['deg']
        
    request_contenu = {
        'lon': lon,
        'lat': lat,
        'description': description,
        'temp': temp,
        'temp_min': temp_min,
        'temp_max': temp_max,
        'pressure': pressure,
        'humidity': humidity,
        'visibility': visibility,
        'speed': speed,
        'deg': deg
    }
    
    print(request_contenu)
    return request_contenu


if __name__ == '__main__':
    extract_weather_data()

    