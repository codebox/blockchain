from blockchain.common.blockchain import Blockchain
from blockchain.common.block import Block
from blockchain.common.transaction import Transaction

import json

TEXT_ENCODING = 'UTF-8'

def text_to_bytes(text):
    return text.encode(TEXT_ENCODING)

def bytes_to_text(bytes):
    return bytes.decode(TEXT_ENCODING)

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

        block.transactions = map(transaction_decode, obj.get('transactions'))
        block.nonce = obj.get('nonce')

        return block

def block_encode(block):
    return json.dumps({'transactions' : map(transaction_encode, block.transactions), 'nonce' : block.nonce})


def transaction_decode(transaction_data):
    obj = json.loads(transaction_data)

    transaction = Transaction(obj['from_address'], obj['amount'], obj['to_address'])
    transaction.signature = obj['signature'];
    return transaction

def transaction_encode(transaction):
    return json.dumps(transaction)
