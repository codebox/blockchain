from blockchain.wallet.network import Network
from blockchain.common.blockchain_loader import BlockchainLoader
from blockchain.common.utils import text_to_bytes, bytes_to_text
from blockchain.common.encoders import block_list_decode
import logging

class BlockchainUpdater:
    def __init__(self, on_valid_block = lambda b: b):
        self.on_valid_block = on_valid_block

    def handle_status_update(self, blockchain_length, host, port):
        def request_blocks_after(blockchain, block_id):
            new_blocks = self._get_new_blocks(host, port, block_id)
            for new_block in new_blocks:
                blockchain.add_block(new_block)
                self.on_valid_block(new_block)
            logging.info('Received {} new blocks from {}:{}'.format(len(new_blocks), host, port))

            return len(new_blocks)

        def update_blockchain(blockchain):
            if blockchain_length > len(blockchain.blocks):
                while not request_blocks_after(blockchain, blockchain.get_last_block_id()):
                    blockchain.remove_last_block()

            else:
                logging.debug('Host {}:{} has {} blocks, ignoring because we already have {}'.format(
                    host, port,blockchain_length, len(blockchain.blocks)
                ))

        BlockchainLoader().process(update_blockchain)

    def _get_new_blocks(self, host, port, last_block_id):
        last_block_id_bytes = text_to_bytes(last_block_id)
        new_blocks_bytes = Network().send_block_request_and_wait(last_block_id_bytes, host, port)
        if len(new_blocks_bytes):
            new_blocks_json = bytes_to_text(new_blocks_bytes)
            return block_list_decode(new_blocks_json)
        else:
            # Unknown block requested, so probably the chain has forked
            return []
