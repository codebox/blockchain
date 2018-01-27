class SendCommand:
    NAME  = 'send'
    USAGE = '{} <amount> <address>'.format(NAME)

    def __init__(self, *args):
        if len(args) != 2:
            print('wrong number of args for {}'.format(SendCommand.NAME))

        else:
            amount, address = args
            print('sending {} to {}'.format(amount, address))