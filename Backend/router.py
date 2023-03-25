from flask import Blueprint, jsonify, request
from flask import Response
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from config_db import db,client, collectionRequest,collectionClient
from flask import Flask, request
from consumer_db import extract_weather_data
import requests
import datetime
from flask_mail import Mail,Message
from http.client import REQUEST_TIMEOUT
from flask import Flask, request
import requests
from kafka import KafkaProducer
import json
from twilio.rest import Client

app = Flask(__name__)

# Configuration du gmail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'zeineb.zayet1@gmail.com'
app.config['MAIL_PASSWORD'] = 'nkbbcbrtemlrwzxj'
mail = Mail(app)

# Configuration du compte Twilio
account_sid = 'ACff76ec96baefd9705289f8efee3d14a6'
auth_token = 'aa6bc5e3db1de35738d780268ee7c9ef'
twilio_phone_number = '+14754738423'


@app.route('/exist_client/<email>', methods=['GET'])
def exist_client(email):
    client = db.collectionClient.find_one({'email': email})
    if client:
        return "True"
    else:
        return "False"
    
@app.route('/recuperateLocation/<location>', methods=['GET'])
def produce_weather_data(location):
    # API endpoint to retrieve weather data
    api_key = "ca91930c630c938d7c31adc91c997a40"
    #location = "London,UK"
    #location = request.json.get('location')
    print(location)
    API_ENDPOINT = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}"

    # Replace city_name and API_KEY with the desired city and API key
    response = requests.get(API_ENDPOINT) 
    weather_data = response.json()  #hiya json

    # Create a Kafka producer
    producer = KafkaProducer(bootstrap_servers=['kafka:9092'],api_version=(0, 10, 0))

    # Convert the weather data to a string and send it to the Kafka broker
    producer.send('weather_topic',value=json.dumps(weather_data).encode('utf-8'))
    producer.flush()

    



@app.route('/register', methods=['POST'])
def register():
    # Récupérer les données de l'utilisateur à partir de la requête POST
    username = request.json.get('username')
    email = request.json.get('email')
    password = request.json.get('password')
    tel=request.json.get('tel')
    # Générer le hash du mot de passe de l'utilisateur
    hashed_password = generate_password_hash(password, method='sha256')
    # Vérifier si l'utilisateur existe déjà dans la base de données
    if db.collectionClient.find_one({'email': email}) is not None:
        return jsonify({'error': 'User with this email already exists.'})
    # Ajouter l'utilisateur à la base de données
    db.collectionClient.insert_one({'username': username, 'email': email, 'password': hashed_password,'tel': tel})
    return jsonify({'message': 'User created successfully.'})



@app.route('/login', methods=['POST'])
def login():
    # Récupérer les données de l'utilisateur à partir de la requête POST
    email = request.json.get('email')
    password = request.json.get('password')
    # Récupérer l'utilisateur correspondant à l'e-mail à partir de la base de données
    user = db.collectionClient.find_one({'email': email})
    # Vérifier si l'utilisateur existe et si le mot de passe est correct
    if user is not None and check_password_hash(user['password'], password):
        return jsonify({'message': 'User logged in successfully.'})
    else:
        return jsonify({'error': 'Invalid email or password.'})





@app.route('/insert_request', methods=['POST'])
def insert_request():

    now = datetime.datetime.now()
    formatted_date = now.strftime("%d-%m-%Y %H:%M:%S")

    email=None
    ville=None

    # Get the data from the request
    email = request.json['email']  
    ville = request.json['ville']
    verif=exist_client(email)
    request_contenu=extract_weather_data()
    if verif=="True" or email==None:
    # Create a document to insert
        new_doc = {'email': email,'contenu': request_contenu,'ville': ville, 'date': formatted_date}

        # Insert the document into the collection
        result = db.collectionRequest.insert_one(new_doc)

        # Return a response indicating the success or failure of the insert
        if result.inserted_id:
            return {'message': 'Request inserted successfully'}
        else:
            return {'error': 'Failed to insert request'}
    else :
        return {'error': 'client does not exist'}
       
@app.route('/get_historique/<email>', methods=['GET'])
def get_historique(email):

    # Récupération des données en fonction de l'id du client
    reqs = db.collectionRequest.find({'email': email})

    # Si aucune requête n'est trouvée
    if  db.collectionRequest.count_documents({'email': email}) == 0:
        return jsonify({'error': 'Client non trouvé'}), 404

    # Récupération du contenu et de la ville de chaque requête
    result = []
    for req in reqs:
        contenu = req.get('contenu')
        ville = req.get('ville')
        date=req.get('date')
        result.append({'contenu': contenu, 'ville': ville,'date':date})

    return json.dumps({'data': result})




@app.route('/alert', methods=['GET'])
def receive_alert():
    temp_min=0
    temp_max=40
    for client in db.collectionClient.find():
        tel = client['tel']
        email = client['email']
        name = client['username']
        print(email)
        response = get_historique(email)

        parsed_response = json.loads(response)
        villes = []
        for item in parsed_response['data']:
            ville=item['ville']
            villes.append(ville)
            produce_weather_data(ville)
            request_contenu=extract_weather_data()
            temp=request_contenu['temp']
            temp = temp - 273.15
            if(temp>=temp_max or temp<=temp_min):
                send_email(email,name,ville,temp)
                send_sms(name,tel,ville,temp)
        print(villes)
    return villes

@app.route('/send_email',methods=['GET'])
def send_email(email,name,ville,temp): 
    recipient = email
    subject = 'Alert Weather Email'
    body = f"""
Bonjour {name}, 

This is an email to inform you that {ville} has a temperature of {temp}°C ! Please be aware and take necessary precautions.

Thank you.

Best regards,
Zeineb
"""
    sender = app.config['MAIL_USERNAME']
    msg = Message(subject=subject, body=body, sender=sender, recipients=[recipient])
    mail.send(msg)
    return 'Email sent!'

@app.route('/send_sms', methods=['GET'])
# Route pour envoyer un SMS
def send_sms(name,tel,ville,temp):
    # Message
    message = f'This is an SMS to inform you that {ville} has a temperature of {temp}°C ! Please be aware and take necessary precautions.'
    # Envoi du SMS
    client_message = f'Bonjour {name}, {message}'
    client_message = client_message[:160]  # Limite le message à 160 caractères pour les SMS
    client_message = client_message.strip()
    twilio_client = Client(account_sid, auth_token)
    twilio_client.messages.create(
        body=client_message,
        from_=twilio_phone_number,
        to = '+216' + str(tel)
    )
    # Retourne un message de confirmation
    return 'SMS envoyé' 

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5005,debug=True)