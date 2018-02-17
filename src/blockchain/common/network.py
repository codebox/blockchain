from socket import *

PORT = 2606
BROADCAST_ADDRESS = '255.255.255.255'

class Network:
    def __init__(self):
        pass

    def send(self, data):
        s = socket(AF_INET, SOCK_DGRAM)
        s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        s.sendto(bytes(data, 'UTF-8'), (BROADCAST_ADDRESS, PORT))

    def download_new_blocks(self, last_known_block):
        print('NET: downloading blocks')
