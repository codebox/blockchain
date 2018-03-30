from threading import Event
from queue import Queue
import logging
import signal, sys

from blockchain.common.config import config
from blockchain.miner.services.block_server import BlockServer
from blockchain.miner.services.status_broadcaster import StatusBroadcaster
from blockchain.common.services.status_listener import StatusListener
from blockchain.common.services.blockchain_updater import BlockchainUpdater
from blockchain.common.crypto import Crypto
from blockchain.miner.services.transaction_listener import TransactionListener
from blockchain.miner.services.block_miner import BlockMiner
from blockchain.common.blockchain_loader import BlockchainLoader
from blockchain.common.config import update_config_from_args

KEY_NAME = 'mining_rewards'

class MiningServer:
    def __init__(self):
        self.shutdown_event = Event()
        self.stop_mining_event = Event()

        block_server_port = config.get('block_server_port')
        self.block_server = BlockServer(block_server_port, self.shutdown_event)

        status_broadcast_port = config.get('status_broadcast_port')
        status_broadcast_interval_seconds = config.get('status_broadcast_interval_seconds')
        self.status_broadcaster = StatusBroadcaster(status_broadcast_port, block_server_port,
                                                    status_broadcast_interval_seconds, self.shutdown_event)

        self.blockchain_updater = BlockchainUpdater(self._on_new_block_downloaded)

        status_listener_port = config.get('status_broadcast_port')
        self.status_listener = StatusListener(status_listener_port, self.shutdown_event, self._on_new_status)

        crypto = Crypto()
        key = crypto.get_key(KEY_NAME) or crypto.generate_key(KEY_NAME)
        self.work_queue = Queue()
        difficulty = config.get('difficulty')
        block_size = config.get('block_size')
        block_reward = config.get('block_reward')
        block_reward_from_address = config.get('block_reward_from')
        self.block_miner = BlockMiner(key, self.work_queue, difficulty, block_size, block_reward, block_reward_from_address,
                                      self.shutdown_event, self.stop_mining_event, self._on_new_block_mined)

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

    def _on_new_block_mined(self, block):
        BlockchainLoader().process(lambda blockchain : blockchain.add_block(block))

    def _on_new_block_downloaded(self, block):
        # we got a new block from elsewhere, stop mining current block someone else beat us to it
        self.stop_mining_event.set()

    def _on_new_transaction(self, transaction):
        self.work_queue.put(transaction)

    def _on_new_status(self, blockchain_length, host, port):
        self.blockchain_updater.handle_status_update(blockchain_length, host, port)

if __name__ == '__main__':
    args = update_config_from_args(sys.argv)

    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

    MiningServer().start()
