import sys
import logging

from blockchain.wallet.commands.send import SendCommand
from blockchain.wallet.commands.make_address import MakeAddressCommand
from blockchain.wallet.commands.list_addresses import ListAddressesCommand
from blockchain.wallet.commands.sync import SyncCommand
from blockchain.common.config import update_config_from_args

COMMANDS = [SendCommand, MakeAddressCommand, ListAddressesCommand, SyncCommand]
USAGE = ' | '.join(map(lambda c : c.USAGE, COMMANDS))

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    if len(sys.argv) < 2:
        logging.info('Usage: python {} ({})'.format(sys.argv[0], USAGE))

    else:
        args = update_config_from_args(sys.argv)
        user_command_name = args[1]
        user_command = None
        for command in COMMANDS:
            if user_command_name == command.NAME:
                user_command = command

        if user_command:
            user_command(*args[2:])
        else:
            logging.error('Unknown command: {}'.format(user_command_name))

