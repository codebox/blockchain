from blockchain.common.crypto import Crypto
from blockchain.common.config import config
from blockchain.common.blockchain_loader import BlockchainLoader
from blockchain.client.payment_manager import PaymentManager
import os
import logging

class ListAddressesCommand:
    NAME  = 'list-addresses'
    USAGE = '{}'.format(NAME)

    def __init__(self, *args):
        if len(args) != 0:
            logging.error('wrong number of args for {}'.format(ListAddressesCommand.NAME))

        else:
            BlockchainLoader().process(self._show_balances)

    def _show_balances(self, blockchain):
        crypto = Crypto()
        keys = crypto.get_keys()
        print("Found {} address{} in directory '{}':".format(len(keys), '' if len(keys) == 1 else 'es', os.path.abspath(crypto.key_store_dir)))

        unconfirmed_payment_totals = self._get_unconfirmed_payment_totals(map(lambda key : key.address, keys))

        print('{:16} {:12} {:12} {:64}'.format('Key Name', 'Balance', 'Pending', 'Address'))
        print('{:-<16} {:-<12} {:-<12} {:-<64}'.format('', '', '', ''))
        for key in keys:
            print('{:16} {:>12} {:>12} {}'.format(key.name, blockchain.get_balance_for_address(key.address),
                                        unconfirmed_payment_totals.get(key.address) or '', key.address))

    def _get_unconfirmed_payment_totals(self, addresses):
        totals = {}

        for address in addresses:
            totals[address] = 0

        for payment in PaymentManager().get_unconfirmed_payments():
            if payment.from_address in addresses:
                totals[payment.from_address] += payment.amount

        return totals
