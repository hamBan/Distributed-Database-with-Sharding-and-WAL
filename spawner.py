from flask import Flask,jsonify,request
import os

app = Flask(__name__)

@app.route('/spawn', methods = ['POST'])
def home():
    payload = request.get_json()
    n = payload.get('n')
    hostnames = payload.get('hostnames', [])
    print(n,hostnames)
    home_message =  {'n': '100'}
    return home_message, 200

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 7000))
    app.run(debug=True, host='0.0.0.0', port=port)