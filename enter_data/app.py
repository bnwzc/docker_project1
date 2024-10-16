from flask import Flask, request, render_template, redirect
import mysql.connector
import requests

app = Flask(__name__)
app.secret_key = 'splat'


data_list = []

@app.route('/')
def index():
    return render_template('index.html', data_list=data_list)

@app.route('/submit', methods=['POST'])
def submit_data():

    password = request.form['password']
    
    auth_response = requests.post('http://auth:5003/auth', json={
        'password': password
    })
    
    if auth_response.status_code != 200 :
        return "No"
    height = request.form['height']
    weight = request.form['weight']
    name = request.form['name'] 
    data_list.append({'name': name, 'height': int(height), 'weight': int(weight), "BMI": round(float(weight) / (float(height) / 100 * float(height) / 100), 2)})
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


