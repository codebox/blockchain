class Block:
    def __init__(self):
        self.transactions = []
        self.nonce = []

    def add(self, transaction):
        self.transactions.append(transaction)

    def set_nonce(self, nonce):
        self.nonce = nonce
