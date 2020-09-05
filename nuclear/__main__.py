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

    # install package [-v version]
    install = subparsers.add_parser(
        'install', help='Install an ArkScript package from GitHub'
    )
    install.add_argument('package', help='Should look like this: user/repo')
    install.add_argument(
        '-v', '--version',
        help='Specify a version for the package'
    )

    # remove package [-v version] [-g|--globally]
    remove = subparsers.add_parser(
        'remove', help='Remove an ArkScript package'
    )
    remove.add_argument('package', help='Should look like this: user/repo')
    remove.add_argument(
        '-v', '--version',
        help='Specify a version for the package'
    )
    remove.add_argument(
        '-g', '--globally',
        help='Remove a package from the local repositories. If not specified' + \
            'remove a package from the current project packages list.'
    )

    args = parser.parse_args()

    if args.subparsers == 'install':
        return install_handler(args)
    elif args.subparsers == 'remove':
        return remove_handler(args)

    return 0


if __name__ == '__main__':
    sys.exit(main())