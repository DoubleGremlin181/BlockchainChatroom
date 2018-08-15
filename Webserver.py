from flask import Flask, jsonify, request
from uuid import uuid4
import Blockchain
import datetime
import json

app = Flask(__name__)
node_identifier = str(uuid4()).replace('-', '')
blockchain = [Blockchain.create_genesis_block(datetime.datetime.now())]  #TODO Make genisis not run on every boot
                                                                         #TODO Allow syncing with a different server

@app.route('/new_block', methods=['POST'])
def new_block():
    values = request.get_json()
    required = ['text']
    if not all(k in values for k in required):
        return 'Missing values', 400

    blockchain.append(Blockchain.create_new_block(blockchain[-1], datetime.datetime.now(), values['text']))

    response = {'message': f'Message successfully added at index: {blockchain[-1].index}'}
    return jsonify(response), 201

@app.route('/chain', methods=['GET'])
def chain():
    values = request.get_json()
    if 'index' in values :
        if 'index' > -(len(blockchain) - 1)and 'index' < len(blockchain):
            return blockchain[values['index']], 200    #TODO Jsonify and fix indexing
        else:
            response = {'message': 'Index out of bounds'}
            return jsonify(response), 400
    else:
        return blockchain[-1], 200  # TODO Jsonify



#print(jsonify({'Index': blockchain[0].index, 'Data': blockchain[0].data, 'Hash': blockchain[0].hash,
#             'Previous_Hash': blockchain[0].previous_hash, 'Timestamp': blockchain[0].timestamp}))
#TODO use json library