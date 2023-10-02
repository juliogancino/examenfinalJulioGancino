
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

import os
load_dotenv()

user = os.getenv('MONGO_USER')
pas = os.getenv('MONGO_PASS')

uri = f"mongodb+srv://juliogancino:4u8G3IVxDd905cnW@clusterciber.mpi0qkr.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

