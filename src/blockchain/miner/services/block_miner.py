from threading import Thread
import logging
import math
from blockchain.common.hash import hash_string, hash_string_to_hex
from blockchain.common.encoders import block_encode
from blockchain.common.block import Block
from blockchain.common.crypto import Crypto
from blockchain.common.blockchain_loader import BlockchainLoader
from blockchain.common.services.transaction_helper import build_transaction

SERVICE_NAME = 'Miner'
STOP_WORKING = None

class BlockMiner(Thread):
    def __init__(self, key, work_queue, difficulty, block_size, block_reward, block_reward_from_address, shutdown_event, on_new_block):
        Thread.__init__(self)
        self.key = key
        self.work_queue = work_queue
        self.required_leading_zero_bits = difficulty
        self.block_size = block_size
        self.block_reward = block_reward
        self.block_reward_from_address = block_reward_from_address
        self.shutdown_event = shutdown_event
        self.on_new_block = on_new_block
        self.current_unmined_block = Block()

    def run(self):
        logging.info('{} started'.format(SERVICE_NAME))

        while not self.shutdown_event.is_set():
            self.current_unmined_block.previous_block_id = self._get_last_block_id_from_blockchain()
            if self.current_unmined_block.is_mineable():
                mining_reward_transaction = self._build_mining_reward_transaction()
                self.current_unmined_block.add(mining_reward_transaction)

                logging.info('{} started mining new block'.format(SERVICE_NAME))
                mined_block = self._mine(self.current_unmined_block)
                mined_block.id = hash_string_to_hex(block_encode(mined_block))
                logging.info('{} mined new block! nonce={} id={}'.format(SERVICE_NAME, str(mined_block.nonce), mined_block.id))
                self.current_unmined_block = Block()
                self.on_new_block(mined_block)

            logging.info('{} waiting for work...'.format(SERVICE_NAME))
            work_item = self.work_queue.get()

            if work_item == STOP_WORKING:
                break

            transaction = work_item
            if not Crypto.validate_transaction(transaction):
                logging.warning('{} received invalid transaction (invalid signature)'.format(SERVICE_NAME))
                continue

            if self.current_unmined_block.has_transaction(transaction):
                logging.info('{} ignoring transaction, already added to current block'.format(SERVICE_NAME))
                continue

            if self._is_transaction_already_in_blockchain(transaction):
                logging.info('{} ignoring transaction, already in blockchain'.format(SERVICE_NAME))
                continue

            self.current_unmined_block.add(transaction)

        logging.info('{} shut down'.format(SERVICE_NAME))

    def stop(self):
        self.work_queue.put(STOP_WORKING)

    def _build_mining_reward_transaction(self):
        return build_transaction(self.block_reward_from_address, self.block_reward,
                                 self.key.address, self.key)

    def _get_last_block_id_from_blockchain(self):
        return BlockchainLoader().process(lambda blockchain : blockchain.get_last_block_id())

    def _is_transaction_already_in_blockchain(self, transaction):
        return BlockchainLoader().process(lambda blockchain : blockchain.has_transaction(transaction))

    def _mine(self, block):
        nonce = 0
        while not self.shutdown_event.is_set():
            block.nonce = nonce

            hash_as_bytes = hash_string(block_encode(block))
            leading_zero_bits = self._count_leading_zero_bits_in_bytes(hash_as_bytes)

            if leading_zero_bits >= self.required_leading_zero_bits:
                block.nonce = nonce
                return block

            nonce += 1

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

    def is_mined(self, block):
        block_hash_bytes = hash_string(block_encode(block))
        leading_zero_bits = self._count_leading_zero_bits_in_bytes(block_hash_bytes)
        return leading_zero_bits >= self.required_leading_zero_bits