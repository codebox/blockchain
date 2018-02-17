from blockchain.common.transaction import Transaction
from blockchain.common.network import Network
from blockchain.common.blockchain import Blockchain
from blockchain.common.crypto import Crypto
from blockchain.common.encoders import transaction_encode

import re

ADDRESS_PATTERN = re.compile('^[a-f0-9]{64}$')
KEY_STORE_DIR = '.' # TODO repeated

class SendCommand:
    NAME  = 'send'
    USAGE = '{} <from address> <amount> <to address>'.format(NAME)

    def __init__(self, *args):
        if len(args) != 3:
            print('wrong number of args for {}'.format(SendCommand.NAME))

        else:
            from_address, amount_txt, to_address = args

            if not self._is_valid_address_format(from_address):
                print('invalid from address')

            elif not self._is_valid_address_format(to_address):
                print('invalid to address')

            elif not self._is_valid_amount_format(amount_txt):
                print('invalid amount')

            else:
                key = Crypto(KEY_STORE_DIR).get_key_by_address(from_address)

                if key is None: # TODO whoa nellie, too much nesting
                    print('client does not own specified From Address')

                else:
                    blockchain = Blockchain()
                    balance = blockchain.get_balance_for_address(from_address)
                    amount = float(amount_txt)

                    if balance < amount:
                        print('insufficient funds')

                    else:
                        transaction = Transaction(from_address, amount, to_address)
                        transaction_data_to_sign = transaction.get_details_for_signature()
                        transaction.signature = key.sign(transaction_data_to_sign)

                        encoded_transaction = transaction_encode(transaction.get_details())

                        net = Network()
                        net.send(encoded_transaction)

    def _is_valid_address_format(self, address_candidate):
        return ADDRESS_PATTERN.match(address_candidate)

    def _is_valid_amount_format(self, amount_txt):
        try:
            return float(amount_txt) > 0
        except ValueError:
            return False

