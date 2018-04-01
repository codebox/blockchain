from blockchain.common.utils import text_to_bytes
from blockchain.common.config import config

class Block:
    def __init__(self):
        self.transactions = []
        self.nonce = None
        self.previous_block_id = None
        self.id = None

    def is_mineable(self):
        if self.previous_block_id == config.get('genesis_block_id'):
            return True
        return len(self.transactions) >= config.get('block_size') - 1 # mining reward transaction will be added

    def add(self, transaction):
        self.transactions.append(transaction) # TODO validation, has id and signature

    def has_transaction(self, transaction):
        return next((True for t in self.transactions if t.id == transaction.id), False)

    def set_nonce(self, nonce):
        self.nonce = nonce
