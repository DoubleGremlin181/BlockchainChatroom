from flask import Flask, jsonify, request
from uuid import uuid4
import Blockchain
import datetime
import json

app = Flask(__name__)
node_identifier = str(uuid4()).replace('-', '')
blockchain = [Blockchain.create_genesis_block(datetime.datetime.now())]

@app.route('/new_block', methods=['POST'])
def new_block():
    values = request.get_json()
    required = ['text']
    if not all(k in values for k in required):
        return 'Missing values', 400

    blockchain.append(Blockchain.create_new_block(blockchain[-1], datetime.datetime.now(), values['text']))

    response = {'message': f'Message successfully added at index: {blockchain[-1].index}'}
    return jsonify(response), 201

@app.route('/chain', methods=['GET', 'POST'])
def chain():
    if flask.request.method == 'GET':
        return blockchain, 200 #TODO Make JSON
    else:
        values = request.get_json()
        required = ['from', 'to']
        if not all(k in values for k in required):
            return 'Missing values', 400

        if to > 0 and len(blockchain) < to: #TODO Add proper checks for from and to
            return 'Out of range', 400

        return blockchain[from:to], 201 #TODO Make JSON
