from blockchain.common.config import config
from blockchain.client.unconfirmed_payments import UnconfirmedPayments
from blockchain.common.encoders import transaction_list_encode, transaction_list_decode
import os.path
import logging
from threading import Lock

class UnconfirmedPaymentsLoader:
    lock = Lock()

    def __init__(self, location = None):
        self.payments_store = location or (config.get('blockchain_store').split('.')[0] + '_pending.json')

    def _load(self):
        unconfirmed_payments = UnconfirmedPayments()

        if os.path.isfile(self.payments_store):
            unconfirmed_payments_list = transaction_list_decode(open(self.payments_store).read())
            logging.debug('Loaded {} unconfirmed payments from {}'.format(len(unconfirmed_payments_list), self.payments_store))
            for unconfirmed_payment in unconfirmed_payments_list:
                unconfirmed_payments.add(unconfirmed_payment)

        return unconfirmed_payments

    def _save(self, unconfirmed_payments):
        transaction_list = unconfirmed_payments.payments.values()
        open(self.payments_store, 'w').write(transaction_list_encode(transaction_list))

    def process(self, op):
        UnconfirmedPaymentsLoader.lock.acquire()
        try:
            unconfirmed_payments = self._load()
            result = op(unconfirmed_payments)
            self._save(unconfirmed_payments)
            return result
        finally:
            UnconfirmedPaymentsLoader.lock.release()