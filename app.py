from flask import Flask, request, jsonify
from pymongo import MongoClient
import time
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client["sensor_data"]
collection = db["readings"]

@app.route('/send_data', methods=['POST'])
def send_data():
    data = request.get_json()
    
    temperature = data.get('temperature')
    humidity = data.get('humidity')
    
    document = {
        "temperature": temperature,
        "humidity": humidity,
        "timestamp": time.time()
    }
    
    collection.insert_one(document)
    
    return jsonify({"status": "success", "message": "Data berhasil disimpan!"})

if __name__ == '__main__':
    app.run(host=os.getenv('FLASK_APP_HOST', '0.0.0.0'), port=int(os.getenv('FLASK_APP_PORT', 5000)))
