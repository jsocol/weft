import argparse


def make_option(*args, **kwargs):
    return (args, kwargs)


class BaseCommand(object):
    command = None
    command_options = ()
    help = ''

    def get_arguments(self, subparsers):
        if self.command is None:
            _, _, self.command = self.__module__.rpartition('.')
        parser = subparsers.add_parser(self.command, help=self.help)
        for (args, kwargs) in self.command_options:
            parser.add_argument(*args, **kwargs)
            parser.set_defaults(func=self.handle)

    def handle(self, options):
        """Subclasses must implement this method."""
        raise NotImplementedError
