from blockchain.common.blockchain import Blockchain
from blockchain.common.block import Block

import json

def blockchain_decode(blockchain_data):
    obj = json.loads(blockchain_data)

    blockchain = Blockchain()
    for obj_child in obj:
        block = block_decode(obj_child)
        blockchain.blocks.append(block)

    return blockchain


def blockchain_encode(blockchain):
    return json.dumps([block_encode(block) for block in blockchain])


def block_decode(block_data):
    obj = json.loads(block_data)

    if obj.get('transactions') and obj.get('nonce'):
        block = Block()

        block.transactions = obj.get('transactions')
        block.nonce = obj.get('nonce')

        return block


def block_encode(block):
    return json.dumps({'transactions' : block.transactions, 'nonce' : block.nonce})
