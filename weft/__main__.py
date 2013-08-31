import argparse
import os
from importlib import import_module


def build_parser():
    parser = argparse.ArgumentParser('weft')
    return parser


def find_commands(cmd_dir):
    return [f[:-3] for f in os.listdir(cmd_dir) if not
            f.startswith('_') and f.endswith('.py')]


def load_commands(cmd_path, commands):
    cmds = []
    for c in commands:
        mod = import_module('.'.join((cmd_path, c)))
        cmds.append(mod.Command())
    return cmds


def main():
    parser = build_parser()
    commands = load_commands('weft.commands', find_commands('weft/commands'))
    subparsers = parser.add_subparsers()
    [c.get_arguments(subparsers) for c in commands]
    options = parser.parse_args()
    if getattr(options, 'func'):
        return options.func(options)
    return parser.print_help()


if __name__ == '__main__':
    main()
