from blockchain.common.config import config
from blockchain.common.blockchain import Blockchain
from blockchain.common.block import Block
from blockchain.common.encoders import blockchain_encode, blockchain_decode
import os.path
import logging
from threading import Lock

class BlockchainLoader:
    lock = Lock()

    def __init__(self, location = None):
        self.blockchain_store = location or config.get('blockchain_store')

    def _load(self):
        if os.path.isfile(self.blockchain_store):
            blockchain = blockchain_decode(open(self.blockchain_store).read())
            logging.debug('Loaded {} blocks from {}'.format(len(blockchain.blocks), self.blockchain_store))
            return blockchain
        else:
            blockchain = Blockchain()
            genesis_block = Block()
            genesis_block.id = config.get('genesis_block_id')
            genesis_block
            blockchain.blocks.append(genesis_block)
            logging.info('No blockchain found, initialised new chain with genesis block')
            return blockchain

    def _save(self, blockchain):
        open(self.blockchain_store, 'w').write(blockchain_encode(blockchain))

    def process(self, op):
        BlockchainLoader.lock.acquire()
        try:
            blockchain = self._load()
            result = op(blockchain)
            self._save(blockchain)
            return result
        finally:
            BlockchainLoader.lock.release()