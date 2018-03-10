import sys
import logging

from blockchain.client.commands.send import SendCommand
from blockchain.client.commands.make_address import MakeAddressCommand
from blockchain.client.commands.list_addresses import ListAddressesCommand
from blockchain.client.commands.sync import SyncCommand

COMMANDS = [SendCommand, MakeAddressCommand, ListAddressesCommand, SyncCommand]
USAGE = ' | '.join(map(lambda c : c.USAGE, COMMANDS))

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    if len(sys.argv) < 2:
        logging.info('Usage: python {} ({})'.format(sys.argv[0], USAGE))

    else:
        user_command_name = sys.argv[1]
        user_command = None
        for command in COMMANDS:
            if user_command_name == command.NAME:
                user_command = command

        if user_command:
            user_command(*sys.argv[2:])
        else:
            logging.error('Unknown command: {}'.format(user_command_name))

