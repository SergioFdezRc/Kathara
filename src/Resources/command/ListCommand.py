import argparse

from ..foundation.command.Command import Command
from ..manager.ManagerProxy import ManagerProxy
from ..strings import strings, wiki_description


class ListCommand(Command):
    __slots__ = ['parser']

    def __init__(self):
        Command.__init__(self)

        parser = argparse.ArgumentParser(
            prog='kathara list',
            description=strings['list'],
            epilog=wiki_description,
            add_help=False
        )

        parser.add_argument(
            '-h', '--help',
            action='help',
            default=argparse.SUPPRESS,
            help='Show an help message and exit.'
        )

        parser.add_argument(
            '-n', '--name',
            metavar='MACHINE_NAME',
            required=False,
            help='Show only information about a specified machine.'
        )

        self.parser = parser

    def run(self, current_path, argv):
        args = self.parser.parse_args(argv)

        if args.name:
            print(ManagerProxy.get_instance().get_machine_info(args.name))
        else:
            lab_info = ManagerProxy.get_instance().get_lab_info()

            print(next(lab_info))
