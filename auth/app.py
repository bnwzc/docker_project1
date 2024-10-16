from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = 'splat'

CORS(app)

@app.route('/auth', methods=['POST'])
def auth():
    try:
        data = request.json
        password = data.get("password")

        if password and (password.lower() == "hesitation"):
            return jsonify({"message": "Authenticated"}), 200 
        else:
            return jsonify({"message": "Authentication failed"}), 403
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
