# Create a blockchain

import datetime
import hashlib
import json
from flask import Flask, jsonify

# 1. Building a blockchain


class Blockchain:
    # Constructor
    def __init__(self):
        self.chain = []
        self.create_block(proof=1, prev_hash="0")

    # Create a new block that links to the previous one int he chain
    def create_block(self, proof, prev_hash):
        # create a dictionary which contains the information of a block
        block = {
            "index": len(self.chain) + 1,
            "timestamps": str(datetime.datetime.now()),
            "proof": proof,
            "prev_hash": prev_hash,
        }
        self.chain.append(block)
        return block

    # get the last block of the current chain
    def get_prev_block(self):
        return self.chain[-1]  # negative indexing in python

    # PoW algorithm use prev_proof to calculate the current block's proof value
    def proof_of_work(self, prev_proof):
        new_proof = 1
        check_proof = False

        while check_proof is False:
            # should not use symetric operation inside encrypt algorithm (add, ...)
            # Example:
            # prev = 7, new = 5 -> hash(12)
            # prev = 5, new = 7 -> hash(12)
            # => 2 different inputs return the same output
            hash_operation = hashlib.sha256(str(new_proof**2 - prev_proof**2).encode()).hexdigest()
            # .encode() to convert the string to byte string for sha256
            # Require: cryptographic hash starting with 4 leading 0s
            if hash_operation[:4] == "0000":
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    # get the hash value of a block
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        # .dumps() convert a python dictionary to json format
        # sort_keys = True means sort the keys in the dictionary alphabetically
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):
        prev_block = chain[0]  # starts with genesis block
        block_index = 1  # current block is 1 index more than prev_block
        while block_index < len(chain):
            block = chain[block_index]

            # check if prev_hash of the current block == hash of prev_block
            if block["prev_hash"] != self.hash(prev_block):
                return False

            # check if cryptographic hash starting with 4 leading 0s
            prev_proof = prev_block["proof"]
            curr_proof = block["proof"]
            hash_operation = hashlib.sha256(str(curr_proof**2 - prev_proof**2).encode()).hexdigest()
            if hash_operation[:4] != "0000":
                return False

            # update to validate next blocks
            prev_block = block
            block_index += 1
        return True


# 2. Mining in blockchain

# Creating a web app
app = Flask(__name__)

# Creating a Blockchain
blockchain = Blockchain()
