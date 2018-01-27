class MakeAddressCommand:
    NAME  = 'address'
    USAGE = '{}'.format(NAME)

    def __init__(self, *args):
        if len(args) != 0:
            print('wrong number of args for {}'.format(MakeAddressCommand.NAME))

        else:
            print('new address')