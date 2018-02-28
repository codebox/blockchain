from threading import Thread
from queue import Queue

from blockchain.common.network import Network
from blockchain.common.encoders import transaction_decode
from blockchain.common.utils import bytes_to_text, text_to_bytes
from blockchain.common.crypto import Crypto
from blockchain.common.block import Block
from blockchain.miner.miner import Miner
from blockchain.common.hash import hash_to_hex
from blockchain.common.config import config
import signal, sys

class MiningServer:
    def __init__(self, mining_thread_count):
        self.current_unmined_block = Block()
        self.mining_thread_count = mining_thread_count
        self.mining_threads = []
        self.work_queue = Queue()

    def _quit(self, signal, frame):
        print("Stopping")
        sys.exit(0)

    def start(self):
        signal.signal(signal.SIGINT, self._quit)
        for id in range(self.mining_thread_count):
            t = Thread(target=self.mine_block, args=(id,), daemon=True)
            self.mining_threads.append(t)
            t.start()

        Network().receive_transaction(self.on_transaction)

    def log(self, msg):
        print(msg)

    def mine_block(self, thread_id):
        self.log('Mining thread {} started'.format(thread_id))
        while True:
            unmined_block = self.work_queue.get()
            self.log('Mining thread {} active'.format(thread_id))
            miner = Miner(config.get('difficulty'))
            miner.mine(unmined_block)
            mined_block = unmined_block
            self.log('New block mined! nonce={} hash={}'.format((str(mined_block.nonce)), hash_to_hex(mined_block.to_bytes())))

    def format_address(self, address):
        return address[:12] + '...'

    def on_transaction(self, transaction_bytes):
        transaction_text = bytes_to_text(transaction_bytes)
        transaction = transaction_decode(transaction_text)

        self.log('New Transaction: {} from {} to {}'.format(
            transaction.amount, self.format_address(transaction.from_address), self.format_address(transaction.to_address)))

        if self.validate_transaction(transaction):
            self.log('Transaction is valid')
            self.current_unmined_block.transactions.append(transaction)
            if self.current_unmined_block.is_mineable():
                self.work_queue.put(self.current_unmined_block)
                self.current_unmined_block = Block()
            else:
                tc = len(self.current_unmined_block.transactions)
                self.log('Current block has {} unmined transaction{}'.format(str(tc), '' if tc == 1 else 's'))
        else:
            self.log('Transaction is invalid')

    def validate_transaction(self, transaction):
        signature = transaction.signature
        public_key = text_to_bytes(transaction.public_key)
        transaction_details = text_to_bytes(transaction.get_details_for_signature())
        return Crypto.validate_signature(transaction_details, public_key, signature)

if __name__ == '__main__':
    MiningServer(3).start()
