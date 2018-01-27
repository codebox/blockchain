from blockchain.common.crypto import Crypto

KEY_STORE_DIR = '.'

class MakeAddressCommand:
    NAME  = 'new-address'
    USAGE = '{}'.format(NAME)

    def __init__(self, *args):
        if len(args) != 1:
            print('wrong number of args for {}'.format(MakeAddressCommand.NAME))

        else:
            key_name = args[0]
            try:
                _, key_file_path = Crypto(KEY_STORE_DIR).generate_key(key_name)
                print('Generated [{}] address, keys are saved in {}'.format(key_name, key_file_path))
            except BaseException as e:
                print('ERROR: {}'.format(e))
