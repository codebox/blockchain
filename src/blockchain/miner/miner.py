import math
from blockchain.common.hash import hash_string
from blockchain.common.encoders import block_encode

class Miner:
    def __init__(self, leading_zero_bits):
        self.required_leading_zero_bits = leading_zero_bits

    def count_leading_zero_bits_in_byte(self, b):
        return 8 - math.floor(math.log(b, 2)) - 1 if b else 8

    def count_leading_zero_bits_in_bytes(self, bytes):
        count = 0

        for b in bytes:
            leading_zero_bits_in_byte = self.count_leading_zero_bits_in_byte(b)
            count += leading_zero_bits_in_byte
            if leading_zero_bits_in_byte < 8:
                return count

        return count

    def mine(self, block):
        nonce = 0
        while True:
            block.nonce = nonce

            hash_as_bytes = hash_string(block_encode(block))
            leading_zero_bits = self.count_leading_zero_bits_in_bytes(hash_as_bytes)

            if leading_zero_bits >= self.required_leading_zero_bits:
                return nonce

            nonce += 1

    def is_mined(self, block):
        block_hash_bytes = hash_string(block_encode(block))
        leading_zero_bits = self.count_leading_zero_bits_in_bytes(block_hash_bytes)
        return leading_zero_bits >= self.required_leading_zero_bits

