from http.client import REQUEST_TIMEOUT
from flask import Flask, request
import requests
from kafka import KafkaProducer
import json

app = Flask(__name__)

@app.route('/recuperateLocation', methods=['GET'])
def produce_weather_data():
    # API endpoint to retrieve weather data
    api_key = "ca91930c630c938d7c31adc91c997a40"
    #location = "London,UK"
    location = request.json.get('location')
    print(location)
    API_ENDPOINT = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}"

    # Replace city_name and API_KEY with the desired city and API key
    response = requests.get(API_ENDPOINT) 
    weather_data = response.json() 

    # Create a Kafka producer
    producer = KafkaProducer(bootstrap_servers=['kafka:9092'],api_version=(0, 10, 0))

    # Convert the weather data to a string and send it to the Kafka broker
    producer.send('weather_topic',value=json.dumps(weather_data).encode('utf-8'))
    producer.flush()

    #print(json.dumps(weather_data).encode('utf-8'))
if __name__ == '__main__':
    #produce_weather_data()
    app.run(host='0.0.0.0',debug=True)
    