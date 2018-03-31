from blockchain.common.crypto import Crypto
import logging

KEY_STORE_DIR = '.'

class MakeAddressCommand:
    NAME  = 'new-address'
    USAGE = '{} <address name>'.format(NAME)

    def __init__(self, *args):
        if len(args) != 1:
            logging.error('wrong number of args for {}'.format(MakeAddressCommand.NAME))

        else:
            key_name = args[0]
            try:
                key = Crypto().generate_key(key_name)
                logging.info('Generated key [{}] with address {}. Key saved in {}'.format(key.name, key.address, key.key_file_path))
            except BaseException as e:
                logging.error(e)
