from blockchain.common.transaction import Transaction
from blockchain.common.crypto import Crypto
from blockchain.common.encoders import transaction_encode
from blockchain.common.utils import text_to_bytes
from blockchain.common.blockchain_loader import BlockchainLoader
from blockchain.client.network import Network

import re
import logging

ADDRESS_PATTERN = re.compile('^[a-f0-9]{64}$')

class SendCommand:
    NAME  = 'send'
    USAGE = '{} <from address> <amount> <to address>'.format(NAME)

    def __init__(self, *args):
        if len(args) != 3:
            logging.error('wrong number of args for {}'.format(SendCommand.NAME))

        else:
            from_address_or_key, amount_txt, to_address_or_key = args

            crypto = Crypto()
            key = crypto.get_key(from_address_or_key) or crypto.get_key_by_address(from_address_or_key)

            if not key:
                logging.error('invalid from address/key')

            elif not (crypto.get_key(to_address_or_key) or self._is_valid_address_format(to_address_or_key)):
                logging.error('invalid to address/key')

            elif not self._is_valid_amount_format(amount_txt):
                logging.error('invalid amount')

            else:
                balance = BlockchainLoader().process(lambda b : b.get_balance_for_address(key.address))
                amount = float(amount_txt)

                if balance < amount:
                    logging.error('insufficient funds') #TODO improve msg

                else:
                    to_address_key = crypto.get_key(to_address_or_key)
                    if to_address_key:
                        to_address = to_address_key.address
                    else:
                        to_address = to_address_or_key

                    transaction = Transaction(key.address, amount, to_address, key.get_public_key())
                    transaction_data_to_sign = transaction.get_details_for_signature()
                    transaction.signature = key.sign(transaction_data_to_sign)

                    encoded_transaction_text = transaction_encode(transaction)
                    encoded_transaction_bytes = text_to_bytes(encoded_transaction_text)

                    Network().send_transaction(encoded_transaction_bytes)

    def _is_valid_address_format(self, address_candidate):
        return ADDRESS_PATTERN.match(address_candidate)

    def _is_valid_amount_format(self, amount_txt):
        try:
            return float(amount_txt) > 0
        except ValueError:
            return False

