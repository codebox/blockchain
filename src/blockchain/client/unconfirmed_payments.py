class UnconfirmedPayments:
    def __init__(self):
        self.payments = {}

    def add(self, transaction):
        self.payments[transaction.id] = transaction

    def get(self):
        return self.payments

    def remove(self, transaction):
        if transaction.id in self.payments:
            del self.payments[transaction.id]