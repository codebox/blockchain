from blockchain.client.network import Network
from blockchain.common.services.blockchain_updater import BlockchainUpdater
import signal
import logging
from threading import Event

class SyncCommand:
    NAME  = 'sync'
    USAGE = '{}'.format(NAME)

    def __init__(self, *args):
        if len(args) != 0:
            logging.error('wrong number of args for {}'.format(SyncCommand.NAME))

        else:
            self.shutdown_event = Event()

            on_status_update = BlockchainUpdater().handle_status_update
            self.listener = Network().find_host_to_sync(on_status_update, self.shutdown_event)

            signal.signal(signal.SIGINT, self._quit)

    def _quit(self, signal, frame):
        self.shutdown_event.set()
        self.listener.close()
