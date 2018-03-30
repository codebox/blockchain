from socket import *
from threading import Thread
from blockchain.common.utils import bytes_to_text
import logging
import sys

SERVICE_NAME = 'Status Listener'
BUFFER_SIZE = 1024
BACKLOG_SIZE = 3

class StatusListener(Thread):
    def __init__(self, listener_port, shutdown_event, on_update):
        Thread.__init__(self)
        self.listener_port = listener_port
        self.shutdown_event = shutdown_event
        self.on_update = on_update

    def run(self):
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.socket.setsockopt(SOL_SOCKET, SO_REUSEPORT, 1)
        self.socket.bind(('', self.listener_port))
        logging.info('{} listening for status updates on port {}...'.format(SERVICE_NAME, self.listener_port))

        while not self.shutdown_event.is_set():
            try:
                bytes, addr = self.socket.recvfrom(BUFFER_SIZE)
                status_value, block_server_port = bytes_to_text(bytes).split(':')
                host = addr[0]
                logging.debug('{} received new status update of {} from {}:{}'.format(SERVICE_NAME, status_value, host, block_server_port))
                self.on_update(int(status_value), host, int(block_server_port))

            except OSError:
                logging.debug('{} error: {}'.format(SERVICE_NAME, sys.exc_info()))
                pass # probably close() was called

            except Exception:
                logging.error('{} error: {}'.format(SERVICE_NAME, sys.exc_info()))

        logging.info('{} shut down'.format(SERVICE_NAME))

    def close(self):
        self.socket.close()
