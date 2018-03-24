from blockchain.client.network import Network
from blockchain.common.blockchain_loader import BlockchainLoader
from blockchain.common.utils import text_to_bytes, bytes_to_text
from blockchain.common.encoders import block_list_decode
import signal
import logging
from threading import Event

class SyncCommand:
    NAME  = 'sync'
    USAGE = '{}'.format(NAME)

    def __init__(self, *args):
        if len(args) != 0:
            logging.error('wrong number of args for {}'.format(SyncCommand.NAME))

        else:
            self.shutdown_event = Event()
            self.listener = Network().find_host_to_sync(self.on_sync_host_found, self.shutdown_event)
            signal.signal(signal.SIGINT, self._quit)

    def _quit(self, signal, frame):
        self.shutdown_event.set()
        self.listener.close()

    def on_sync_host_found(self, host, port):
        def update_blockchain(blockchain):
            last_block_id = blockchain.get_last_block_id()
            new_blocks = self._get_new_blocks(host, port, last_block_id)
            logging.info('Received {} new blocks from {}:{}'.format(len(new_blocks), host, port))
            for new_block in new_blocks:
                blockchain.add_block(new_block)

        BlockchainLoader().process(update_blockchain)

    def _get_new_blocks(self, host, port, last_block_id):
        last_block_id_bytes = text_to_bytes(last_block_id)
        new_blocks_bytes = Network().send_block_request_and_wait(last_block_id_bytes, host, port)
        new_blocks_json = bytes_to_text(new_blocks_bytes) # TODO handle empty response (unknown block)
        return block_list_decode(new_blocks_json)
