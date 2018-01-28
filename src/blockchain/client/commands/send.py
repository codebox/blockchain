from blockchain.common.transaction import Transaction
from blockchain.common.network import Network

class SendCommand:
    NAME  = 'send'
    USAGE = '{} <amount> <address>'.format(NAME)

    def __init__(self, *args):
        if len(args) != 3:
            print('wrong number of args for {}'.format(SendCommand.NAME))

        else:
            from_address, amount, to_address = args
            t = Transaction(from_address, amount, to_address)
            net = Network()
            net.send_transaction(t)