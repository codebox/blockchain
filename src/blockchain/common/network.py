from blockchain.common.encoders import text_to_bytes
from socket import *

TRANSACTION_PORT = 2606
BROADCAST_ADDRESS = '255.255.255.255'
BUFFER_SIZE = 10 * 1024

class Network:
    def __init__(self):
        pass

    def send_transaction(self, bytes):
        s = socket(AF_INET, SOCK_DGRAM)
        s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        s.sendto(bytes, (BROADCAST_ADDRESS, TRANSACTION_PORT))

    def receive_transaction(self, on_transaction):
        s = socket(AF_INET, SOCK_DGRAM)
        s.setsockopt(SOL_SOCKET, SO_REUSEPORT, 1) # allows multiple miners on same host
        s.bind(('', TRANSACTION_PORT))

        while True:
            bytes, _ = s.recvfrom(BUFFER_SIZE)
            on_transaction(bytes)

    def download_new_blocks(self, last_known_block):
        print('NET: downloading blocks')
