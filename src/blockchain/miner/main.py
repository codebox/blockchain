from threading import Thread, Event
from queue import Queue
import logging
import signal, sys

from blockchain.common.config import config
from blockchain.miner.services.block_server import BlockServer
from blockchain.miner.services.status_broadcaster import StatusBroadcaster
from blockchain.common.services.status_listener import StatusListener
from blockchain.common.crypto import Crypto
from blockchain.miner.services.transaction_listener import TransactionListener
from blockchain.miner.services.block_miner import BlockMiner
from blockchain.common.blockchain_loader import load, save

KEY_NAME = 'mining_rewards'

class MiningServer:
    def __init__(self):
        self.shutdown_event = Event()

        block_server_port = config.get('block_server_port')
        self.block_server = BlockServer(block_server_port, self.shutdown_event)

        status_broadcast_port = config.get('status_broadcast_port')
        status_broadcast_interval_seconds = config.get('status_broadcast_interval_seconds')
        self.status_broadcaster = StatusBroadcaster(status_broadcast_port, status_broadcast_interval_seconds, self.shutdown_event)

        status_listener_port = config.get('status_broadcast_port')
        self.status_listener = StatusListener(status_listener_port, self.shutdown_event)

        crypto = Crypto()
        key = crypto.get_key(KEY_NAME) or crypto.generate_key(KEY_NAME)
        self.work_queue = Queue()
        difficulty = config.get('difficulty')
        block_size = config.get('block_size')
        block_reward = config.get('block_reward')
        block_reward_from_address = config.get('block_reward_from_address')
        self.block_miner = BlockMiner(key, self.work_queue, difficulty, block_size, block_reward, block_reward_from_address,
                                      self.shutdown_event, self._on_new_block)

        transaction_listener_port = config.get('transaction_port')
        self.transaction_listener = TransactionListener(transaction_listener_port, self.shutdown_event, self._on_new_transaction)

    def _quit(self, signal, frame):
        logging.info("Stopping...")
        self.shutdown_event.set()
        self.block_server.close()
        self.status_listener.close()
        self.transaction_listener.close()
        self.block_miner.stop()

    def start(self):
        signal.signal(signal.SIGINT, self._quit)

        # Miners do several jobs...
        self.status_broadcaster.start()   # tell everyone else the length of the blockchain that we have
        self.block_server.start()         # listen for requests for the latest blockchain (from clients or other miners)
        self.status_listener.start()      # listen for other miners telling us the length of their blockchains
        self.transaction_listener.start() # listen for new transactions from clients
        self.block_miner.start()          # mine new blocks

        self.shutdown_event.wait()
        logging.info("Main thread stopped")

    def _on_new_block(self, block):
        blockchain = load()
        blockchain.add_block(block)
        save(blockchain)

    def _on_new_transaction(self, transaction):
        self.work_queue.put(transaction)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

    MiningServer().start()
