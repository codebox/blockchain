from blockchain.common.config import config
from blockchain.common.blockchain import Blockchain
from blockchain.common.block import Block
from blockchain.common.encoders import blockchain_encode, blockchain_decode
import os.path

def load():
    blockchain_store = config.get('blockchain_store')
    if os.path.isfile(blockchain_store):
        return blockchain_decode(open(blockchain_store).read())
    else:
        blockchain = Blockchain()
        genesis_block = Block()
        genesis_block.id = config.get('genesis_block_id')
        blockchain.blocks.append(genesis_block)
        return blockchain

def save(blockchain):
    open(config.get('blockchain_store'), 'w').write(blockchain_encode(blockchain))
