class Transaction:
    def __init__(self, from_address, amount, to_address):
        self.from_address = from_address
        self.amount = amount
        self.to_address = to_address
        self.signature = None

    def sign(self, signature):
        self.signature = signature

    def get_details_for_signature(self):
        return '{} {} {}'.format(self.from_address, str(self.amount), self.to_address)

    def get_details(self):
        return {
            'from'      : self.from_address,
            'to'        : self.to_address,
            'amount'    : self.amount,
            'signature' : self.signature
        }

    def __repr__(self):
        return '{} --[{}]--> {}'.format(self.from_address, str(self.amount), self.to_address)