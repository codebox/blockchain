class PaymentManager:
    def __init__(self):
        self.payments = {}

    def log_unconfirmed_payment(self, transaction):
        self.payments[transaction.id]

    def get_unconfirmed_payments(self):
        return []

    def log_confirmed_payment(self, transaction):
        pass