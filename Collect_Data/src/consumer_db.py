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

for message in consumer:
             # Insert data into MongoDB
             contenu=message.value
print(contenu)

# traitement 
# test if client exist
#insert request twalli fl router
                     #  historique
"""
app = Flask(_name_)

@app.route('/insert_request', methods=['POST'])
def insert_request():
    # Get the data from the request
    client_mail = request.json['client_mail']   # tester si client exuste reelellement

    contenu = request.json['contenu'] # ml front
    ville = request.json['ville']

    # Get the current system date and time
    now = datetime.now()

    # Create a document to insert
    new_doc = {'client_id': client_id, 'contenu': contenu, 'ville': ville, 'date': now}

    # Insert the document into the collection
    result = collection.insert_one(new_doc)

    # Return a response indicating the success or failure of the insert
    if result.inserted_id:
        return {'message': 'Request inserted successfully'}
    else:
        return {'error': 'Failed to insert request'}

******************



# traiter reponse de l'API ===>> output json
@app.route('/clients/<client_id>', methods=['GET'])
def get_client(client_id):
    clients_collection = client['database_name']['collection_name']
    client = clients_collection.find_one({'_id': client_id})
    if client is not None:
        ville = request.json['ville']
        contenu = request.json['contenu'] # ml front
        # Get the current system date and time
        now = datetime.now()
  
        for message in consumer:
             # Insert data into MongoDB
             collection.insert_one(message.value)



        return True
    else:
        return False


"""