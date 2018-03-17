from socket import *
from threading import Thread
import logging
import sys
from blockchain.common.utils import bytes_to_text
from blockchain.common.encoders import transaction_decode

SERVICE_NAME = 'Transaction Listener'
BUFFER_SIZE = 1024 * 1024
BACKLOG_SIZE = 3

class TransactionListener(Thread):
    def __init__(self, listener_port, shutdown_event, on_new_transaction):
        Thread.__init__(self)
        self.listener_port = listener_port
        self.shutdown_event = shutdown_event
        self.on_new_transaction = on_new_transaction

    def run(self):
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.socket.setsockopt(SOL_SOCKET, SO_REUSEPORT, 1)
        self.socket.bind(('', self.listener_port))
        logging.info('{} listening for new transactions on port {}...'.format(SERVICE_NAME, self.listener_port))

        while not self.shutdown_event.is_set():
            try:
                bytes, addr = self.socket.recvfrom(BUFFER_SIZE)
                transaction_text = bytes_to_text(bytes)
                transaction = transaction_decode(transaction_text)

                logging.info('{} received new transaction for amount {} from {}'.format(SERVICE_NAME, transaction.amount, addr[0]))
                self.on_new_transaction(transaction)

            except OSError:
                logging.debug('{} error: {}'.format(SERVICE_NAME, sys.exc_info()))
                pass # probably close() was called

            except Exception:
                logging.error('{} error: {}'.format(SERVICE_NAME, sys.exc_info()))

        logging.info('{} shut down'.format(SERVICE_NAME))

    def close(self):
        self.socket.close()
