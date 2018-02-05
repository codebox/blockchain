class Network:
    def __init__(self):
        pass

    def send_transaction(self, transaction):
        print('NET: sending transaction [{}]'.format(transaction))

    def download_new_blocks(self, last_known_block):
        print('NET: downloading blocks')
