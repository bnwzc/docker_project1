from flask import Flask, request, render_template, redirect, session, url_for
import mysql.connector
import yaml
import os
import json
import requests

current_dir = os.path.dirname(os.path.abspath(__file__))
user_file_path = os.path.join(current_dir, 'user.yml')
accounts_file_path = os.path.join(current_dir, 'accounts.json')
app = Flask(__name__)
app.secret_key = 'splat'

with open(user_file_path, 'r') as f:
    user = yaml.safe_load(f.read())
with open(accounts_file_path, 'r') as f:
    accounts = json.load(f)

data_list = []

@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html', data_list=data_list)
    return redirect(url_for('login'))

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

@app.route('/submit', methods=['POST'])
def submit_data():
    if 'username' not in session:
        return redirect(url_for('login'))

    height = request.form['height']
    weight = request.form['weight']
    name = request.form['name']
    
    data_list.append({'name': name, 'height': height, 'weight': weight})
    db_conn = None
    db_cursor = None
    try:
        db_conn = mysql.connector.connect(
            host='mysql_db',
            user='root',
            password='root',
            database='project'
        )
        db_cursor = db_conn.cursor()
        query = "INSERT INTO height_weight (name, height, weight) VALUES (%s, %s, %s)"
        db_cursor.execute(query, (name, height, weight))

        db_conn.commit()

        requests.post('http://analytics:5002/analytics', json={})

    except mysql.connector.Error as err:
        return f"Error: {err}"
    finally:
        db_cursor.close()
        db_conn.close()

    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


