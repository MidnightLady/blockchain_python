import datetime
import hashlib
import json
from flask import Flask, jsonify


class Blockchain:
    chain = None
    difficulty = 1
    busy = False

    def __init__(self, difficulty=1):
        self.chain = []
        self.difficulty = difficulty
        self.__create_genesis_block()

    def __create_genesis_block(self):
        data = "hello, world!"
        self._create_block(data, "0")

    def _create_block(self, data, previous_hash):
        self.busy = True
        hash_data = self._hash_function(data)
        header_block = {"index": len(self.chain),
                        "timestamp": str(datetime.datetime.now().timestamp()),
                        "hash_data": hash_data,
                        "difficulty": self.difficulty,
                        "nonce": 0,
                        "previous_hash": previous_hash, }
        header_block, _hash = self._mining(header_block)

        new_block = {
            "header": header_block,
            "block_hash": _hash,
            "data": data,
        }
        self.chain.append(new_block)
        self.busy = False
        return new_block

    def add_block(self, data):
        last_block = self.chain[-1]
        self._create_block(data, last_block["block_hash"])

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty if difficulty >= 1 else 1

    def get_target(self, difficulty):
        return "".zfill(difficulty)

    def _hash_function(self, data):
        encode_data = json.dumps(data, sort_keys=True).encode()
        return hashlib.sha256(encode_data).hexdigest()

    def _mining(self, header_block):
        target = self.get_target(header_block["difficulty"])
        while True:
            _hash = self._hash_function(header_block)
            if _hash.startswith(target):
                return header_block, _hash
            else:
                header_block["nonce"] += 1
                if header_block["nonce"] > abs(0xffffffff):
                    header_block["nonce"] = 0
                    header_block["timestamp"] = str(datetime.datetime.now().timestamp())

    def valid_chain(self):
        previous_block = None
        for block in self.chain:
            header = block["header"]
            if previous_block and header["previous_hash"] != previous_block["block_hash"]:
                return False

            hash_data = self._hash_function(block["data"])
            if hash_data != header["hash_data"]:
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
        blocks = []
        for block in self.chain:
            blocks.append(("block " + str(block["header"]["index"]) + " : " + block["block_hash"], block["data"]))
        return blocks
