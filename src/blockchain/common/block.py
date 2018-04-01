from blockchain.common.config import config
from blockchain.common.hash import hash_string
import blockchain.common.encoders
import math

class Block:
    def __init__(self):
        self.transactions = []
        self.nonce = None
        self.previous_block_id = None
        self.id = None

    def add(self, transaction):
        self.transactions.append(transaction)

    def has_transaction(self, transaction):
        return next((True for t in self.transactions if t.id == transaction.id), False)

    def set_nonce(self, nonce):
        self.nonce = nonce

    def is_mineable(self):
        if self.previous_block_id == config.get('genesis_block_id'):
            return True
        return len(self.transactions) >= config.get('block_size') - 1 # mining reward transaction will be added

    def is_mined(self):
        block_hash_bytes = hash_string(blockchain.common.encoders.block_encode(self, False))
        leading_zero_bits = self._count_leading_zero_bits_in_bytes(block_hash_bytes)
        return leading_zero_bits >= config.get('difficulty')

    def _count_leading_zero_bits_in_bytes(self, bytes):
        count = 0

        for b in bytes:
            leading_zero_bits_in_byte = self._count_leading_zero_bits_in_byte(b)
            count += leading_zero_bits_in_byte
            if leading_zero_bits_in_byte < 8:
                return count

        return count

    def _count_leading_zero_bits_in_byte(self, b):
        return 8 - math.floor(math.log(b, 2)) - 1 if b else 8
