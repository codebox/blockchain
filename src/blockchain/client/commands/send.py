from blockchain.common.transaction import Transaction
from blockchain.common.network import Network
from blockchain.common.blockchain import Blockchain
from blockchain.common.crypto import Crypto
from blockchain.common.encoders import transaction_encode
from blockchain.common.utils import text_to_bytes

import re

ADDRESS_PATTERN = re.compile('^[a-f0-9]{64}$')

class SendCommand:
    NAME  = 'send'
    USAGE = '{} <from address> <amount> <to address>'.format(NAME)

    def __init__(self, *args):
        if len(args) != 3:
            print('wrong number of args for {}'.format(SendCommand.NAME))

        else:
            from_address_or_key, amount_txt, to_address = args

            crypto = Crypto()
            key = crypto.get_key(from_address_or_key) or crypto.get_key_by_address(from_address_or_key)

            if not key:
                print('invalid from address/key')

            elif not self._is_valid_address_format(to_address):
                print('invalid to address')

            elif not self._is_valid_amount_format(amount_txt):
                print('invalid amount')

            else:
                blockchain = Blockchain()
                balance = blockchain.get_balance_for_address(key.address)
                amount = float(amount_txt)

                if balance < amount:
                    print('insufficient funds')

                else:
                    transaction = Transaction(key.address, amount, to_address, key.get_public_key())
                    transaction_data_to_sign = transaction.get_details_for_signature()
                    transaction.signature = key.sign(transaction_data_to_sign)

                    encoded_transaction_text = transaction_encode(transaction.get_details())
                    encoded_transaction_bytes = text_to_bytes(encoded_transaction_text)

                    net = Network()
                    net.send_transaction(encoded_transaction_bytes)

    def _is_valid_address_format(self, address_candidate):
        return ADDRESS_PATTERN.match(address_candidate)

    def _is_valid_amount_format(self, amount_txt):
        try:
            return float(amount_txt) > 0
        except ValueError:
            return False

