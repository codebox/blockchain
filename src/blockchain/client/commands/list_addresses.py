from blockchain.common.crypto import Crypto
from blockchain.common.config import config
import os

class ListAddressesCommand:
    NAME  = 'list-addresses'
    USAGE = '{}'.format(NAME)

    def __init__(self, *args):
        if len(args) != 0:
            print('wrong number of args for {}'.format(ListAddressesCommand.NAME))

        else:
            crypto = Crypto()
            keys = crypto.get_keys()
            print("Found {} address{} in directory '{}':".format(len(keys), '' if len(keys) == 1 else 'es', os.path.abspath(crypto.key_store_dir)))
            for key in keys:
                print('* {} - {}'.format(key.name, key.address))
