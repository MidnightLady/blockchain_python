import datetime
import hashlib
import json
import time

import requests
import random

from flask import request

from boot_nodes import boot_nodes


class Blockchain:
    chain = []
    current_difficulty = 4
    busy = False
    nodes = []
    current_node = None
    found_block = False
    reward = 0

    def __init__(self):
        self.current_node = request.host
        self.nodes = [_ for _ in boot_nodes if _ != self.current_node]

        for ip in self.nodes:
            try:
                response = requests.get(f'http://{ip}/get_chain')
                if response.status_code == 200:
                    self.chain = response.json()
                    print(f'Chain retrieved from node {ip}')
                    break
            except Exception as e:
                print(f'Error retrieving chain from {ip}: {e}')
        if not self.chain:
            self.__create_genesis_block()

    def __create_genesis_block(self):
        data = "hello, world!"
        self._create_block(data, "0")

    def _create_block(self, data, previous_hash):
        self.busy = True
        hash_tx = self._hash_function(data)
        header_block = {"index": len(self.chain),
                        "timestamp": str(datetime.datetime.now().timestamp()),
                        "hash_tx": hash_tx,
                        "difficulty": self.current_difficulty,
                        "nonce": random.Random().randint(0, abs(0xffffffff)),
                        "previous_hash": previous_hash, }
        header_block, _hash = self._mining(header_block)
        if _hash is not False:
            self.broadcast_new_block(data, header_block, _hash)
            self.reward += 1
            new_block = {
                "header": header_block,
                "block_hash": _hash,
                "tx": data,
            }
            self.chain.append(new_block)
        self.busy = False

    # assuming new difficulty every new block
    def _calc_new_difficulty(self):
        last_block = self.chain[-1]

    def add_transaction(self, tx):
        self.broadcast_new_transaction(tx)
        self.create_block(tx)

    def create_block(self, tx):
        last_block = self.chain[-1]
        self.found_block = False
        self._create_block(tx, last_block["block_hash"])

    def set_difficulty(self, difficulty):
        self.current_difficulty = difficulty if difficulty >= 1 else 1

    def get_target(self, difficulty):
        return "".zfill(difficulty)

    def _hash_function(self, data):
        encode_data = json.dumps(data, sort_keys=True).encode()
        return hashlib.sha256(encode_data).hexdigest()

    def _mining(self, header_block):
        print("mine", header_block)
        target = self.get_target(header_block["difficulty"])
        while not self.found_block:
            _hash = self._hash_function(header_block)
            if _hash.startswith(target):
                return header_block, _hash
            else:
                header_block["nonce"] += 1
                if header_block["nonce"] > abs(0xffffffff):
                    header_block["nonce"] = 0
                    header_block["timestamp"] = str(datetime.datetime.now().timestamp())
        return False, False

    def valid_chain(self):
        previous_block = None
        for block in self.chain:
            header = block["header"]
            if previous_block and header["previous_hash"] != previous_block["block_hash"]:
                return False

            hash_tx = self._hash_function(block["tx"])
            if hash_tx != header["hash_tx"]:
                return False

            block_hash = self._hash_function(header)
            target = self.get_target(header["difficulty"])
            if block_hash != block["block_hash"] or not block_hash.startswith(target):
                return False

            previous_block = block

        return True

    def get_block(self, index):
        return self.chain[index] if len(self.chain) >= index else None

    def get_all_blocks(self):
        return self.chain

    # consensus blockchain network:
    def connect_blockchain_network(self):
        pass

    def add_new_node(self):
        pass

    def broadcast_new_transaction(self, tx):
        for ip in self.nodes:
            try:
                # easiest way to broadcast without waiting for response
                requests.post(f'http://{ip}/receive_transaction', json={'tx': tx}, timeout=0.001)
            except Exception as e:
                pass
        print(f'Transaction broadcasted to {len(self.nodes)} nodes')

    def receive_transaction(self, tx):
        print("receive tx")
        self.create_block(tx)


    def broadcast_new_block(self, data, header_block, _hash):
        for ip in self.nodes:
            try:
                requests.post(f'http://{ip}/receive_block', json={'data': data, 'header_block': header_block, 'hash': _hash}, timeout=0.001)
            except Exception as e:
                pass
        print(f'New Block broadcasted index {header_block['index']}')

    def receive_block(self, data, header_block, _hash):
        if header_block['index'] == len(self.chain) and header_block['previous_hash'] == self.chain[-1]["block_hash"]:
            new_block = {
                "header": header_block,
                "block_hash": _hash,
                "tx": data,
            }
            print("receive block", header_block)
            self.chain.append(new_block)
            self.found_block = True
