import json

from flask import Flask, redirect, request
from pow_blockchain import Blockchain
import os, base64

app = Flask(__name__)
chain: Blockchain = None


@app.route("/", methods=['GET'])
def menu():
    response = "<h1>Current Blockchain :</h1>"
    global chain
    if not chain:
        chain = Blockchain()

    all_blocks = chain.get_all_blocks()
    response += "<h4>Node server: '" + chain.current_node + " Reward: '" + str(chain.reward) + "'</h4>"

    for block in all_blocks:
        b_hash = block["block_hash"][:6] + "..." + block["block_hash"][-4:]
        pre_hash = block["header"]["previous_hash"][:6] + "..." + block["header"]["previous_hash"][-4:]
        response += "<a>Block " + str(block["header"]["index"]) + "</a> : " + b_hash + "<b> previous block: </b> " + pre_hash + "<br/>"
    response += "<a>check: " + "Valid!" if chain.valid_chain() else "Invalid!!!" + "</a><br/>"
    response += "<h4>Current difficulty: '" + chain.get_target(chain.current_difficulty) + "'</h4>"
    response += "<br/><h4>MENU: </h4><br/>"
    response += "<a href='/add_transaction'>Add new transaction</a><br/><br/>"

    return response


@app.route("/add_transaction", methods=['GET'])
def add_transaction():
    chain.add_transaction(base64.b64encode(os.urandom(16)).decode())
    return redirect('/')


@app.route("/receive_transaction", methods=['POST'])
def receive_transaction():
    tx = request.json.get('tx')
    chain.receive_transaction(tx)
    return redirect('/')


@app.route("/get_chain", methods=['GET'])
def get_chain():
    return json.dumps(chain.get_all_blocks())


@app.route("/receive_block", methods=['POST'])
def receive_block():
    data = request.json.get('data')
    header_block = request.json.get('header_block')
    _hash = request.json.get('hash')
    chain.receive_block(data, header_block, _hash)
    return redirect('/')
