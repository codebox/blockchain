from blockchain.common.crypto import Crypto

KEY_STORE_DIR = '.'

class ListAddressesCommand:
    NAME  = 'list-addresses'
    USAGE = '{}'.format(NAME)

    def __init__(self, *args):
        if len(args) != 0:
            print('wrong number of args for {}'.format(ListAddressesCommand.NAME))

        else:
            keys = Crypto(KEY_STORE_DIR).get_keys()
            print("Found {} address{} in directory '{}':".format(len(keys), '' if len(keys) == 1 else 'es', KEY_STORE_DIR))
            for name in keys.keys():
                print('* {}'.format(name))
