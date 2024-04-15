from flask import Flask,jsonify,request
import json
import os
import requests
import socket
import sqlite3

app = Flask(__name__)

all_shards = {} # Format : {server name : [shard list]}
all_servers = {} # Format : {shard : [server list]}
primary_servers = {} # Format : {shard : primary server}

def elect_primary(shard):
    max_seq = 0
    max_server = ''
    for server in all_servers[shard]:
        logfile = open(server+'.json')
        log = json.load(logfile)
        for seq_num in log:
            if log[seq_num]['shard_id'] == shard and seq_num > max_seq:
                max_seq = seq_num
                max_server = server
        logfile.close()
    primary_servers[shard] = max_server

def update_log(server):
    logfile = open(server+'.json')
    log = json.load(logfile)
    logfile.close()
    for shard in all_shards[server]:
        primary_logfile = open(primary_servers[shard]+'.json')
        primary_log = json.load(primary_logfile)
        primary_logfile.close()
        max_seq_present = 0
        for seq_num in log:
            if log[seq_num]['shard_id'] == shard and seq_num > max_seq_present:
                max_seq_present = seq_num
            elif log[seq_num]['shard_id'] == shard and log[seq_num]['is_committed'] == 0:
                url = f'http://{server}:5000/{primary_log[seq_num]['operation_name']}'
                data = primary_log[seq_num]['operation_name']
                if primary_log[seq_num]['operation_name'] == 'update':
                    requests.put(url, json=data)
                elif primary_log[seq_num]['operation_name'] == 'write':
                    requests.post(url, json=data)
                elif primary_log[seq_num]['operation_name'] == 'del':
                    requests.delete(url, json=data)
                log[seq_num]['is_committed'] = 1
        max_seq = 0
        for seq_num in primary_log:
            if primary_log[seq_num]['shard_id'] == shard and seq_num > max_seq_present:
                log[seq_num] = primary_log[seq_num]
                url = f'http://{server}:5000/{primary_log[seq_num]['operation_name']}'
                data = primary_log[seq_num]['operation_name']
                if primary_log[seq_num]['operation_name'] == 'update':
                    requests.put(url, json=data)
                elif primary_log[seq_num]['operation_name'] == 'write':
                    requests.post(url, json=data)
                elif primary_log[seq_num]['operation_name'] == 'del':
                    requests.delete(url, json=data)
                log[seq_num]['is_committed'] = 1
    logfile_write = open(server+'.json','w')
    json.dump(log,logfile_write)
    logfile_write.close()

def replicate_log(server):
    log = {}
    for shard in all_shards[server]:
        primary_logfile = open(primary_servers[shard]+'.json')
        primary_log = json.load(primary_logfile)
        primary_logfile.close()
        for seq_num in primary_log:
            if primary_log[seq_num]['shard_id'] == shard:
                log[seq_num] = primary_log[seq_num]
                url = f'http://{server}:5000/{primary_log[seq_num]['operation_name']}'
                data = primary_log[seq_num]['operation_name']
                if primary_log[seq_num]['operation_name'] == 'update':
                    requests.put(url, json=data)
                elif primary_log[seq_num]['operation_name'] == 'write':
                    requests.post(url, json=data)
                elif primary_log[seq_num]['operation_name'] == 'del':
                    requests.delete(url, json=data)
                log[seq_num]['is_committed'] = 1
            
    logfile_write = open(server+'.json','w')
    json.dump(log,logfile_write)
    logfile_write.close()

@app.route('/init', methods=['GET'])
def init():
    payload = request.get_json()
    
    shards = payload.get('shards')
    return {},200

@app.route('/add', methods=['GET'])
def add():
    payload = request.get_json()
    n = payload['n']

    new_shards = payload.get('new_shards')
    for shard in new_shards:
        all_servers[shard] = []
        elect_primary(shard)
    return {},200

@app.route('/rm', methods=['GET'])
def rm():
    payload = request.get_json()
    try:
        host_ip = socket.gethostbyname('host.docker.internal')
        url = f'http://{host_ip}:7000/remove'
        data = payload
        response = requests.post(url, json=data)
        print('Remove request successful:', response.text)
        response.raise_for_status()
        status = 200
    except requests.exceptions.RequestException as e:
        data = {'message':f'Add failed with error : {e}'}
        status = 500
    return {},status

@app.route('/get_primary', methods=['POST'])
def get_primary():
    return primary_servers