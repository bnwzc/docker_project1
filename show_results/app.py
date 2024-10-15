from flask import Flask, request, render_template, redirect, session, url_for
import mysql.connector
import yaml
import os
import json
import requests
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
    client = MongoClient('mongodb://host.docker.internal:27017/')
    db = client['result']
    collection = db['health_weight']
    
    statistics = collection.find_one({"_id": "statistics"})
    client.close()
    
    return statistics


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in accounts and accounts[username] == password:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return "Wrong password"
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/')
def index():
    if 'username' in session:
        statistics = read_from_mongodb()
        return render_template('results.html', statistics=statistics)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
