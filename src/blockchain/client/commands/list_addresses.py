from blockchain.common.crypto import Crypto
from blockchain.common.config import config
from blockchain.common.blockchain_loader import BlockchainLoader
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
        for key in keys:
            #TODO improve formatting
            print('* {} {} - {}'.format(key.name, blockchain.get_balance_for_address(key.address), key.address))

