from flask import Flask,jsonify,request
import os

app = Flask(__name__)

@app.route('/spawn', methods = ['POST'])
def spawn():
    payload = request.get_json()
    servers = payload['servers']
    for server in servers:
        os.system(f'sudo docker run -d --name {server}_db database')
        os.system(f'sudo docker run -d -e "MYSQL_HOST={server}_db" --network my_network --name {server} server')
    return {},200

@app.route('/remove', methods = ['POST'])
def remove():
    payload = request.get_json()
    servers = payload['servers']
    for server in servers:
        os.system(f'sudo docker rm {server}_db') # incomplete
        os.system(f'sudo docker rm {server}') # incomplete

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 7000))
    app.run(debug=True, host='0.0.0.0', port=port)