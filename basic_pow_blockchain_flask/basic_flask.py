from flask import Flask, jsonify, redirect
from pow_blockchain import Blockchain
import os, base64

app = Flask(__name__)
chain: Blockchain = Blockchain()


@app.route("/", methods=['GET'])
def menu():
    response = "<h1>Current Blockchain :</h1>"

    blocks = chain.get_all_blocks()
    for block in blocks:
        response += "<a>" + block[0] + "</a> message: " + block[1] + "<br/>"
    response += "<a>check: " + "Valid!" if chain.valid_chain() else "Invalid!!!" + "</a><br/>"
    response += "<h4>Current difficulty: '" + chain.get_target(chain.difficulty) + "-'</h4>"
    response += "<br/><h4>MENU: </h4><br/>"
    response += "<a href='/add_block'>Add new block</a><br/><br/>"
    response += "<a href='/increase_difficulty'>Increase difficulty</a><br/><br/>"
    response += "<a href='/decrease_difficulty'>Decrease difficulty</a><br/><br/>"
    response += "<a href='/init_blockchain'>Init new blockchain</a><br/><br/>"

    return response


@app.route("/init_blockchain", methods=['GET'])
def init_blockchain():
    global chain
    chain = Blockchain(chain.difficulty)
    return redirect('/')


@app.route("/add_block", methods=['GET'])
def add_block():
    if not chain.busy:
        chain.add_block(base64.b64encode(os.urandom(16)).decode())
    return redirect('/')


@app.route("/increase_difficulty", methods=['GET'])
def increase_difficulty():
    chain.set_difficulty(chain.difficulty + 1)
    return redirect('/')

@app.route("/decrease_difficulty", methods=['GET'])
def decrease_difficulty():
    chain.set_difficulty(chain.difficulty - 1)
    return redirect('/')

