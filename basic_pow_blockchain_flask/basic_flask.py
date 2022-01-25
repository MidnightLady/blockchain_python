from flask import Flask, jsonify, redirect, request
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
    for block in all_blocks:
        response += "<a>Block " + str(block["header"]["index"]) + "</a> : " + block["block_hash"] + "<b> previous block: </b> " + block["header"]["previous_hash"] + "<br/>"
    response += "<a>check: " + "Valid!" if chain.valid_chain() else "Invalid!!!" + "</a><br/>"
    response += "<h4>Current difficulty: '" + chain.get_target(chain.current_difficulty) + "-'</h4>"
    response += "<br/><h4>MENU: </h4><br/>"
    response += "<a href='/add_transaction'>Add new transaction</a><br/><br/>"

    return response


@app.route("/add_transaction", methods=['GET'])
def add_transaction():
    print(request.environ)
    chain.add_transaction(base64.b64encode(os.urandom(16)).decode())
    return redirect('/')
