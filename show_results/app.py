from flask import Flask, request, render_template, redirect, session, url_for
import os
import json
from flask import Flask, render_template
from pymongo import MongoClient
import os
import yaml

current_dir = os.path.dirname(os.path.abspath(__file__))
user_file_path = os.path.join(current_dir, 'user.yml')
accounts_file_path = os.path.join(current_dir, 'accounts.json')
app = Flask(__name__)
app.secret_key = 'splat'
with open(accounts_file_path, 'r') as f:
    accounts = json.load(f)
def read_from_mongodb():
    client = MongoClient('mongodb://root:root@mongo_db:27017/')
    db = client['project']
    collection = db['statistics']
    
    statistics = collection.find_one({"_id": "statistics"})
    client.close()
    
    return statistics


@app.route('/')
def index():
    statistics = read_from_mongodb()
    return render_template('results.html', statistics=statistics)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
