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
        max_seq = 0
        for seq_num in primary_log:
            if primary_log[seq_num]['shard_id'] == shard and seq_num > max_seq_present:
                log[seq_num] = primary_log[seq_num]
                url = f'http://{server}:7000/{primary_log[seq_num]['operation_name']}'
                data = primary_log[seq_num]['operation_name']
                if primary_log[seq_num]['operation_name'] == 'update':
                    requests.put(url, json=data)
                elif primary_log[seq_num]['operation_name'] == 'write':
                    requests.post(url, json=data)
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
    logfile_write = open(server+'.json','w')
    json.dump(log,logfile_write)
    logfile_write.close()

@app.route('/init', methods=['POST'])
def init():
    payload = request.get_json()
    n = payload.get('N')
    schema = payload.get('schema')
    # code for server creation to be added
    shards = payload.get('shards')
    data = {}
    return jsonify(data),200

@app.route('/add', methods=['POST'])
def add():
    pass

@app.route('/rm', methods=['POST'])
def rm():
    pass

@app.route('/get_primary', methods=['POST'])
def get_primary():
    return primary_servers