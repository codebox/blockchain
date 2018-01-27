import sys

from commands.send import SendCommand
from commands.make_address import MakeAddressCommand
from commands.sync import SyncCommand

COMMANDS = [SendCommand, MakeAddressCommand, SyncCommand]
USAGE = ' | '.join(map(lambda c : c.USAGE, COMMANDS))

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python {} ({})'.format(sys.argv[0], USAGE))

    else:
        user_command_name = sys.argv[1]
        user_command = None
        for command in COMMANDS:
            if user_command_name == command.NAME:
                user_command = command

        if user_command:
            user_command(*sys.argv[2:])
        else:
            print('Unknown command: {}'.format(user_command_name))

