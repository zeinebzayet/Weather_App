from pymongo import MongoClient
# Set up MongoDB client and database
client = MongoClient('mongodb://172.18.0.7:27017/',username='admin',
                 password='password')


db = client['weatherdatabase']

# Set up MongoDB collections
collectionRequest = db['request']
collectionClient= db['client']


