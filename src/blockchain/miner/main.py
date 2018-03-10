from threading import Thread
from queue import Queue
import logging

from blockchain.common.network import Network
from blockchain.common.encoders import transaction_decode, block_encode
from blockchain.common.utils import bytes_to_text, text_to_bytes
from blockchain.common.crypto import Crypto
from blockchain.common.block import Block
from blockchain.miner.miner import Miner
from blockchain.common.hash import hash_string_to_hex
from blockchain.common.config import config
from blockchain.common.transaction import Transaction
from blockchain.common.blockchain_loader import load, save

import signal, sys

class MiningServer:
    def __init__(self, blockchain, key, mining_thread_count):
        self.current_unmined_block = Block()
        self.blockchain = blockchain
        self.mining_thread_count = mining_thread_count
        self.mining_threads = []
        self.work_queue = Queue()
        self.key = key

    def _quit(self, signal, frame):
        logging.info("Stopping")
        sys.exit(0)

    def start(self):
        signal.signal(signal.SIGINT, self._quit)
        for id in range(self.mining_thread_count):
            t = Thread(target=self.mine_block, args=(id,), daemon=True)
            self.mining_threads.append(t)
            t.start()

        Network().receive_transaction(self.on_transaction)

    def mine_block(self, thread_id):
        logging.info('Mining thread {} started'.format(thread_id))
        miner = Miner(config.get('difficulty'))
        while True:
            unmined_block = self.work_queue.get()
            logging.info('Mining thread {} active'.format(thread_id))
            miner.mine(unmined_block)
            mined_block = unmined_block
            mined_block.id = hash_string_to_hex(block_encode(mined_block))
            self.blockchain.add_block(mined_block)
            save(self.blockchain)
            logging.info('New block mined! nonce={} hash={}'.format((str(mined_block.nonce)), mined_block.id))

    def format_address(self, address):
        return address[:12] + '...'

    def on_transaction(self, transaction_bytes):
        transaction_text = bytes_to_text(transaction_bytes)
        transaction = transaction_decode(transaction_text)

        logging.info('New Transaction: {} from {} to {}'.format(
            transaction.amount, self.format_address(transaction.from_address), self.format_address(transaction.to_address)))

        if self.validate_transaction(transaction):
            logging.info('Transaction is valid')
            self.current_unmined_block.transactions.append(transaction)
            if self.current_unmined_block.is_mineable():
                self.current_unmined_block.previous_block_id = self.blockchain.get_last_block_id()

                # Build the mining reward transaction
                transaction = Transaction(config.get('block_reward_from'),
                                          config.get('block_reward'), self.key.address, self.key.get_public_key())
                transaction_data_to_sign = transaction.get_details_for_signature()
                transaction.signature = self.key.sign(transaction_data_to_sign)

                self.current_unmined_block.transactions.append(transaction)
                self.work_queue.put(self.current_unmined_block)
                self.current_unmined_block = Block()

            else:
                tc = len(self.current_unmined_block.transactions)
                logging.info('Current block has {} unmined transaction{}'.format(str(tc), '' if tc == 1 else 's'))
        else:
            logging.warning('Transaction is invalid')

    def validate_transaction(self, transaction):
        signature = transaction.signature
        public_key = text_to_bytes(transaction.public_key)
        transaction_details = text_to_bytes(transaction.get_details_for_signature())
        return Crypto.validate_signature(transaction_details, public_key, signature)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

    blockchain = load()

    crypto = Crypto()
    KEY_NAME = 'mining_rewards'
    key = crypto.get_key(KEY_NAME) or crypto.generate_key(KEY_NAME)

    MiningServer(blockchain, key, 3).start()
