from flask import Blueprint, jsonify, request
from flask import Response,send_file
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
import bcrypt
from twilio.rest import Client
from flask import Flask
from flask_cors import CORS
from flask import render_template, redirect, url_for,session
from sessionManagment import UserLogged
from crontab import CronTab
from flask_toastr import Toastr
from flask import flash




app=Flask(__name__)
toastr = Toastr(app)
CORS(app,resources={r"/*": {"origins": "*"}})
app.secret_key = "SecretKey"


#  Gmail Configuration 
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'weatherapplication3@gmail.com'
app.config['MAIL_PASSWORD'] = 'jskspxvxudfsmorv'
mail = Mail(app)

# Twilio Configuration
account_sid = 'AC982684b66c9895c8bd74e28fbd53a476'
auth_token = '36804bed2b45618431ef7af48ebc2257'
twilio_phone_number = '+15856326771'


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

    
@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    logged_in = UserLogged()

    # Récupérer l'utilisateur actuellement connecté à partir de la session Flask
    email = session['email']
    print(email)
    if not email:
        return redirect(url_for('login'))

    # Récupérer les informations de l'utilisateur à partir de la base de données
    user = db.collectionClient.find_one({'email': email})

    if request.method == 'POST':
        # Récupérer les nouvelles informations de l'utilisateur à partir du formulaire
        username = request.form.get('username')
        password = request.form.get('password')
        tel = request.form.get('tel')
        
        # Mettre à jour les informations de l'utilisateur dans la base de données
        db.collectionClient.update_one(
            {'email': email},
            {'$set': {'username': username,'password': password, 'tel': tel}}
        )
        
        # Rediriger l'utilisateur vers la page de profil
        return redirect(url_for('edit_profile'))
    else:
           
            return render_template('Edit_Profile.html', user=user,logged_in=logged_in)
    # Afficher le formulaire 
    return render_template('Edit_Profile.html', user=user,logged_in=logged_in)

@app.route('/register', methods=['POST','GET'])
def register():
    logged_in = UserLogged()

    if request.method == 'POST':

        # Récupérer les données de l'utilisateur à partir de la requête POST
        username = request.form.get('username',False)
        email = request.form.get('email',False)
        password = request.form.get('password',False)
        confirm_password = request.form.get('confirm_password',False)
        tel=request.form.get('tel',False)
        user = db.collectionClient.find_one({'email': email})
        if user is None and password == confirm_password:
        
            # Générer le hash du mot de passe de l'utilisateur
            HashPassword = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()) #Hash the password
            #hashed_password = generate_password_hash(password, method='sha256')
            db.collectionClient.insert_one({'username': username, 'email': email, 'password': HashPassword,'tel': tel})
            flash("Account Created Successfully", 'success')
            return redirect("/login") 

        else:
            flash("User with this email already exists", 'error')      
            return render_template("Sign_Up.html",logged_in=logged_in)
            
    else:
       
        return render_template('Sign_Up.html',logged_in=logged_in)
        


# Route pour afficher la page de connexion
@app.route('/login', methods=['GET', 'POST'])
def login():
    logged_in = UserLogged()

    if request.method == 'POST':

        # Récupérer les données de l'utilisateur à partir de la requête POST
        email = request.form.get('email', False)
        print(email)
        password = request.form.get('password', False)

        # Récupérer l'utilisateur correspondant à l'e-mail à partir de la base de données
        user = db.collectionClient.find_one({'email': email})



        if user is not None and bcrypt.checkpw(password.encode("utf-8"), user['password']):
            session["email"] = email
            flash("You are successfully logged in", 'success')
            return redirect("/index") 
        else:
            flash("Email or Password is incorrect", 'error')
            return render_template('Sign_In.html',logged_in=logged_in)
    else:
        return render_template('Sign_In.html',logged_in=logged_in)















# Route pour la page d'accueil
@app.route('/index',methods=['GET'])
def index():
    logged_in = UserLogged()
    if UserLogged():
        # Si l'utilisateur est connecté, affichez la page d'accueil
        return render_template('index.html',logged_in=logged_in)
    else:
        # Sinon, redirigez l'utilisateur vers la page de connexion
        return redirect("/login")

# Route pour se déconnecter
@app.route('/logout')
def logout():
    # Supprimer les données de session de l'utilisateur
    session.pop('email', None)
    return redirect('/login')



@app.route('/response', methods=['GET', 'POST'])
def insert_request():
    logged_in = UserLogged()

    if request.method == 'POST':

        now = datetime.datetime.now()
        formatted_date = now.strftime("%d-%m-%Y %H:%M:%S")

        #email=None
        ville=None
        session["email"]=None 
        # Get the data from the request
        email = session["email"] 
        print("   email f session  *******************")
        print(email)
        ville = request.form.get('ville',False)
        produce_weather_data(ville)
        #verif=exist_client(email)
        user = db.collectionClient.find_one({'email': email})
        request_contenu=extract_weather_data()

        if user is not None or email==None:
           
       
        # Create a document to insert
            new_doc = {'email': email,'contenu': request_contenu,'ville': ville, 'date': formatted_date}
            print("   email ba3d insert  *******************")

            print(email)
            # Insert the document into the collection
            result = db.collectionRequest.insert_one(new_doc)

            # Return a response indicating the success or failure of the insert
            if result.inserted_id:
                temp=request_contenu['temp']
                pressure=request_contenu['pressure']
                speed=request_contenu['speed']
                return render_template("index.html", temp=round(temp- 273.15,2), humidity=request_contenu['humidity'],ville= ville,pressure=round((pressure/2000)*100,2),speed=speed,logged_in=logged_in)
                #return {'message': 'Request inserted successfully'}
            else:
                return {'error': 'Failed to insert request'}
        else :
            return {'error': 'client does not exist'}
    else:
        return render_template('index.html',logged_in=logged_in)
       
@app.route('/get_historique', methods=['GET'])
def get_historique():
    logged_in = UserLogged()

    email=session["email"] 

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
        pressure=contenu['pressure']
        temp=contenu['temp']
        humidity=contenu['humidity']


        print(ville)
        date=req.get('date')
        result.append({'ville': ville,'date':date,'pressure':round((pressure/2000)*100,2),'temp':round(temp- 273.15,2),'humidity':round(humidity,2)})

    return render_template('History.html',result=result,logged_in=logged_in)




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
   

@app.route('/send_email',methods=['GET'])
def send_email(email,name,ville,temp): 
    recipient = email
    subject = 'Alert Weather Email'
    body = f"""
Bonjour {name}, 

This is an email to inform you that {ville} has a temperature of {temp} °C  Please be aware and take necessary precautions.

Thank you.

Best regards,
Weather App Application
"""
    sender = app.config['MAIL_USERNAME']
    msg = Message(subject=subject, body=body, sender=sender, recipients=[recipient])
    mail.send(msg)
    return 'Email sent!'



# Créer une fonction cron qui exécute receive_alert() toutes les 5 minutes
#@app.before_first_request
"""def create_cron_job():
    cron=CronTab(user=session['email'])  
    job = cron.new(command='python /app.py receive_alert')
    job.setall('*/2 * * * *')
    cron.write()"""




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

@app.route('/about',methods=['GET'])
def about():
    logged_in = UserLogged()

    return render_template('about.html',logged_in=logged_in)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5005,debug=True)