# coding: utf-8

import sys
import argparse
from typing import List
import colorama

from .install import handle as install_handler
from .remove import handle as remove_handler


def main() -> int:
    """
    The main function of the program
    """
    colorama.init()

    parser = argparse.ArgumentParser(prog='nuclear', add_help=True)
    subparsers = parser.add_subparsers(dest='subparsers')
    install = subparsers.add_parser(
        'install', help='Install an ArkScript package from GitHub'
    )
    install.add_argument(
        'package',
        help='Should look like this: user/repo'
    )

    remove = subparsers.add_parser(
        'remove', help='Remove an ArkScript package'
    )

    args = parser.parse_args()
    print(args)

    if args.subparsers == 'install':
        return install_handler(args)
    elif args.subparsers == 'remove':
        return remove_handler(args)

    return 0


if __name__ == '__main__':
    sys.exit(main())