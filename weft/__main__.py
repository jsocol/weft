import argparse
import os
from fabric.api import env, execute
from fabric.context_managers import settings
from importlib import import_module


def build_parser():
    parser = argparse.ArgumentParser('weft')
    parser.add_argument('-v', '--verbosity', action='store', dest='verbosity',
                        type=int, default=1)
    parser.add_argument('-H', '--hosts', action='store', dest='hosts', type=str,
                        default='')
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

    arg_hosts = [h.strip() for h in options.hosts.split(',')]

    if getattr(options, 'func'):
        args = [options.func, options]
        execute(options.func,
                hosts=arg_hosts,
                *args)


if __name__ == '__main__':
    main()
