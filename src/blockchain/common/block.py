from blockchain.common.utils import text_to_bytes
from blockchain.common.config import config

class Block:
    def __init__(self):
        self.transactions = []
        self.nonce = []

    def is_mineable(self):
        return len(self.transactions) == config.get('block_size')

    def add(self, transaction):
        self.transactions.append(transaction)

    def set_nonce(self, nonce):
        self.nonce = nonce

    def to_bytes(self):
        return text_to_bytes('|'.join([str(t.get_details()) for t in self.transactions] + [str(self.nonce)]))
