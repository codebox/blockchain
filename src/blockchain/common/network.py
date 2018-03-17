from socket import *
import logging

TRANSACTION_PORT = 2608
BLOCK_PORT = 2607
BROADCAST_ADDRESS = '255.255.255.255'
BUFFER_SIZE = 1024 * 1024

class Network:
    def __init__(self):
        pass

    def send_transaction(self, bytes):
        s = socket(AF_INET, SOCK_DGRAM)
        s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        s.sendto(bytes, (BROADCAST_ADDRESS, TRANSACTION_PORT))

    def receive_transactions(self, on_transaction):
        s = socket(AF_INET, SOCK_DGRAM)
        s.setsockopt(SOL_SOCKET, SO_REUSEPORT, 1) # allows multiple miners on same host
        s.bind(('', TRANSACTION_PORT))
        logging.info('Listening for new transactions...')

        while True:
            bytes, addr = s.recvfrom(BUFFER_SIZE)
            logging.info('Received new transaction from {}'.format(addr))
            on_transaction(bytes)

    def send_block_request_and_wait(self, bytes, host):
        logging.info('requesting new blocks from {}'.format(host))

        s = socket(AF_INET, SOCK_STREAM)
        s.connect((host, BLOCK_PORT))
        s.send(bytes)
        block_data = s.recv(BUFFER_SIZE)
        s.close()

        logging.info('received new block data from {}: {}'.format(host, block_data))

        return block_data

    def receive_block_requests(self, on_block_request):
        s = socket(AF_INET, SOCK_STREAM)
        s.bind(('', BLOCK_PORT))
        s.listen(1)
        logging.info('Listening for new blocks requests...')

        while True:
            conn, addr = s.accept()
            logging.info('Received new blocks request from {}'.format(addr))
            bytes = conn.recv(BUFFER_SIZE)
            on_block_request(conn, bytes)

    def find_host_to_sync(self, on_host_found):
        on_host_found('localhost') #TODO