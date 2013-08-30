import argparse
import os


def build_parser():
    parser = argparse.ArgumentParser('weft')
    return parser


def find_commands(cmd_dir):
    return [f[:-3] for f in os.listdir(cmd_dir) if not
            f.startswith('_') and f.endswith('.py')]
