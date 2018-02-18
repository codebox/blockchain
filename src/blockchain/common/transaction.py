class Transaction:
    def __init__(self, from_address, amount, to_address, public_key):
        self.from_address = from_address
        self.amount = amount
        self.to_address = to_address
        self.public_key = public_key
        self.signature = None

    def get_details_for_signature(self):
        return '{} {} {}'.format(self.from_address, str(self.amount), self.to_address)

    def get_details(self):
        return {
            'from_address' : self.from_address,
            'to_address'   : self.to_address,
            'amount'       : self.amount,
            'public_key'   : self.public_key,
            'signature'    : self.signature
        }

    def __repr__(self):
        return '{} --[{}]--> {}'.format(self.from_address, str(self.amount), self.to_address)