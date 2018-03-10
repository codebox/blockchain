from blockchain.common.config import config
from blockchain.common.blockchain import Blockchain
from blockchain.common.block import Block
from blockchain.common.encoders import blockchain_encode, blockchain_decode
import os.path
import logging

def load(location = None):
    blockchain_store = location or config.get('blockchain_store')
    if os.path.isfile(blockchain_store):
        blockchain = blockchain_decode(open(blockchain_store).read()) #TODO validate blockchain
        logging.info('Loaded {} blocks from {}'.format(len(blockchain.blocks), blockchain_store))
        return blockchain
    else:
        blockchain = Blockchain()
        genesis_block = Block()
        genesis_block.id = config.get('genesis_block_id')
        blockchain.blocks.append(genesis_block)
        logging.info('No blockchain found, initialised new chain with genesis block')
        return blockchain

def save(blockchain, location = None):
    open(location or config.get('blockchain_store'), 'w').write(blockchain_encode(blockchain))
