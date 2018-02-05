from blockchain.common.transaction import Transaction
from blockchain.common.network import Network
from blockchain.common.blockchain import Blockchain
import re

ADDRESS_PATTERN = re.compile('^[a-f0-9]{64}$')

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
                blockchain = Blockchain()
                balance = blockchain.get_balance_for_address(from_address)
                amount = float(amount_txt)

                if balance is None:
                    print('client does not own specified From Address')

                elif balance < amount:
                    print('insufficient funds')

                else:
                    t = Transaction(from_address, amount, to_address)
                    net = Network()
                    net.send_transaction(t)

    def _is_valid_address_format(self, address_candidate):
        return ADDRESS_PATTERN.match(address_candidate)

    def _is_valid_amount_format(self, amount_txt):
        try:
            amount = float(amount_txt)
            return amount > 0
        except ValueError:
            return False

