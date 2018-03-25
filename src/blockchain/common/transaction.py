class Transaction:
    def __init__(self, from_address, amount, to_address, public_key):
        self.from_address = from_address
        self.amount = amount
        self.to_address = to_address
        self.public_key = public_key
        self.timestamp = None
        self.id = None
        self.signature = None

    def get_details_for_signature(self):
        return '{} {} {} {}'.format(self.from_address, str(self.amount), self.to_address, self.timestamp)

    def __repr__(self):
        return '{} --[{}]--> {}'.format(self.from_address, str(self.amount), self.to_address)