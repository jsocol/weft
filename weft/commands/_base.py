import argparse


def make_option(*args, **kwargs):
    return (args, kwargs)


class BaseCommand(object):
    command = None
    command_options = ()
    help = ''

    @classmethod
    def get_arguments(cls, subparsers):
        if cls.command is None:
            _, _, cls.command = cls.__module__.rpartition('.')
        parser = subparsers.add_parser(cls.command, help=cls.help)
        for (args, kwargs) in cls.command_options:
            parser.add_argument(*args, **kwargs)

    def handle(self, **options):
        """Subclasses must implement this method."""
        raise NotImplementedError
