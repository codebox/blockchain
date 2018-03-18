from socket import *
from threading import Thread
import sys
import logging
from blockchain.common.encoders import block_encode, block_list_encode
from blockchain.common.utils import bytes_to_text, text_to_bytes
from blockchain.common.blockchain_loader import BlockchainLoader

SERVICE_NAME = 'Block Server'
BUFFER_SIZE = 1024 * 1024
BACKLOG_SIZE = 3

class BlockServer(Thread):
    def __init__(self, listener_port, shutdown_event):
        Thread.__init__(self)
        self.listener_port = listener_port
        self.shutdown_event = shutdown_event
        self.socket = None

    def run(self):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.socket.bind(('', self.listener_port))
        self.socket.listen(BACKLOG_SIZE)
        logging.info('{} started, listening on port {}...'.format(SERVICE_NAME, self.listener_port))

        connection = None
        while not self.shutdown_event.is_set():
            try:
                connection, addr = self.socket.accept()
                logging.info('{} received new request from {}'.format(SERVICE_NAME, addr[0]))
                request_bytes = connection.recv(BUFFER_SIZE)
                self._on_block_request(connection, request_bytes)

            except ConnectionAbortedError:
                logging.debug('{} error: {}'.format(SERVICE_NAME, sys.exc_info()))
                pass # probably close() was called

            except Exception:
                logging.error('{} error: {}'.format(SERVICE_NAME, sys.exc_info()))
                if connection:
                    connection.close()

        logging.info('{} shut down'.format(SERVICE_NAME))

    def close(self):
        self.socket.close()

    def _on_block_request(self, connection, request_bytes):
        block_id = bytes_to_text(request_bytes)
        logging.info('{} request for blocks following {}'.format(SERVICE_NAME, block_id))

        new_blocks = BlockchainLoader().process(lambda blockchain : blockchain.get_blocks_following(block_id))

        if new_blocks is not None:
            new_blocks_json = block_list_encode(new_blocks)
            new_blocks_bytes = text_to_bytes(new_blocks_json)
            connection.send(new_blocks_bytes)
            logging.info('{} sent {} new blocks'.format(SERVICE_NAME, len(new_blocks)))
        else:
            logging.info('{} unknown block requested: {}'.format(SERVICE_NAME, block_id))

        connection.close()
