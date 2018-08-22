from flask import Flask, jsonify, request
from uuid import uuid4
import Blockchain
import datetime

app = Flask(__name__)
node_identifier = str(uuid4()).replace("-", "")
blockchain = [Blockchain.create_genesis_block(datetime.datetime.now())]  #TODO Make genisis not run on every boot
                                                                         #TODO Allow syncing and verifying with a different server


def json_block(index):
    return jsonify({"Index": blockchain[index].index, "Data": blockchain[index].data, "Hash": blockchain[index].hash,
                        "Previous_Hash": blockchain[index].previous_hash, "Timestamp": str(blockchain[index].timestamp)})

@app.route("/", methods=["GET"])
def root():
    response = {"Address": [{"/new_block":{"Method": "POST", "Values": "text"}},
                           {"/get_block":{"Method": "GET", "Values": "index"}}]}
    return jsonify(response), 200

@app.route("/new_block", methods=["POST"])
def new_block():
    message_data = request.args.get("text")
    if message_data:
        if len(message_data) < 500:
            blockchain.append(Blockchain.create_new_block(blockchain[-1], datetime.datetime.now(), message_data))
            response = {"message": f"Message successfully added at index: {blockchain[-1].index}"}
            return jsonify(response), 201
        response = {"message": "Message is too big "}
        return jsonify(response), 413
    response = {"message": "Missing values"}
    return jsonify(response), 400

@app.route("/get_block", methods=["GET"])
def get_block():
    index = int(request.args.get("index"))
    if index >= -(len(blockchain)) and index < len(blockchain):
        return json_block(index), 200
    else:
        response = {"message": "Index out of bounds"}
        return jsonify(response), 400

if __name__ == "__main__":
    app.run(debug=True, port=5000)  #TODO Remove