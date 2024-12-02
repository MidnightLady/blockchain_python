import datetime
import hashlib
import json
from boot_nodes import boot_nodes


class Blockchain:
    chain = None
    current_difficulty = 1
    busy = False
    boot_nodes = boot_nodes
    transaction_pools = []


    def __init__(self, difficulty=1):
        self.chain = []
        self.current_difficulty = difficulty
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
                        "nonce": 0,
                        "previous_hash": previous_hash, }
        header_block, _hash = self._mining(header_block)

        new_block = {
            "header": header_block,
            "block_hash": _hash,
            "tx": data,
        }
        self.chain.append(new_block)
        self.busy = False
        return new_block

    # assuming new difficulty every new block
    def _calc_new_difficulty(self):
        last_block = self.chain[-1]


    def add_transaction(self, tx):
        self.transaction_pools = tx
        self.broadcast_new_transaction(tx)

        # last_block = self.chain[-1]
        # self._create_block(tx, last_block["block_hash"])

    def set_difficulty(self, difficulty):
        self.current_difficulty = difficulty if difficulty >= 1 else 1

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
        pass

    def broadcast_new_block(self):
        pass
