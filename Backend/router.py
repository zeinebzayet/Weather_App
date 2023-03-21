from flask import Blueprint, jsonify, request
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from config_db import db,client 
from flask import Flask, request


app = Flask(__name__)

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








        """

# Route pour récupérer les données en fonction de l'id du client
@app.route('/historique/<client_id>', methods=['GET'])
def get_requete(client_id):
    # Récupération des données en fonction de l'id du client
   
    req = collectionRequest.find_one({'client_id': client_id})

    # Si la requête n'est pas trouvée
    if not req:
        return jsonify({'error': 'Client non trouvé'}), 404

    # Récupération du contenu et de la ville
    contenu = req.get('contenu')
    ville = req.get('ville')

    # Retourne les données sous forme de JSON
    return jsonify({'contenu': contenu, 'ville': ville}), 200



    


@users_api.route('/register', methods=['GET'])
def alert_temp():

    consumer_back = KafkaConsumer('weather_topic',
                             bootstrap_servers=['kafka:9092'],
                             auto_offset_reset='earliest',
                             group_id='my-group',
                             value_deserializer=lambda x: json.loads(x.decode('utf-8')),
                             api_version=(0, 10, 0))
# parcourir les clients, chaque client  les pays visites (collection user qui contient les champs username,password,email,pays qui est deja collection fiha libelle w date  w information li hiya collection n7otou fih ma3loumet )
#lancer requete w recuperer json li howa topic o ne5dhou temerature
# test si temperature  tfout on envoie mail/notif en real time

    while True:
        # Response format is {TopicPartiton('topic1', 1): [msg1, msg2]}
        msg_pack = consumer.poll(timeout_ms=500)

        for tp, messages in msg_pack.items():
                for message in messages:
                # message value and key are raw bytes -- decode if necessary!
                # e.g., for unicode: `message.value.decode('utf-8')`
                    print ("%s:%d:%d: key=%s value=%s" % (tp.topic, tp.partition,
                                                        message.offset, message.key,
                                                        message.value))
    # Récupérer la température à partir du topic Weather_APP
    temperature = request.form.get('username')
    
    # Générer le hash du mot de passe de l'utilisateur
    hashed_password = generate_password_hash(password, method='sha256')
    # Vérifier si l'utilisateur existe déjà dans la base de données
    if db.users.find_one({'email': email}) is not None:
        return jsonify({'error': 'User with this email already exists.'})
    # Ajouter l'utilisateur à la base de données
    db.users.insert_one({'username': username, 'email': email, 'password': hashed_password})
    return jsonify({'message': 'User created successfully.'})



def addNumbers(num1, num2, num3):
"""

if __name__ == '__main__':
    #produce_weather_data()
    app.run(host='0.0.0.0',port=5000,debug=True)