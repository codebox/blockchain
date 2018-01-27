class SyncCommand:
    NAME  = 'sync'
    USAGE = '{}'.format(NAME)

    def __init__(self, *args):
        if len(args) != 0:
            print('wrong number of args for {}'.format(SyncCommand.NAME))

        else:
            print('syncing with network')