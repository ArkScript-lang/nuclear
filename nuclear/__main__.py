# coding: utf-8

import sys
import argparse
from typing import List
import colorama

from . import get
from . import log


def is_valid_package_name(name: str) -> bool:
    """
    Check if a given package name is under the form user/repo
    """
    # we need a single /
    if name.count('/') != 1:
        return False
    # we need a valid username and repo name, not user/ or /repo
    if not all(len(e) > 0 for e in name.split('/')):
        return False
    return True


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
        # check for validity
        if not is_valid_package_name(args.package):
            log.error(f"Provided package name is not valid: {args.package}")
            return -1
        # then check for existance on GitHub
        user, repo = args.package.split('/')
        if not get.check_user(user):
            log.error(f"The GitHub user '{user}' doesn't exists")
            return -1
        if not get.check_repo(user, repo):
            log.error(f"The wanted package '{repo}' from {user} couldn't be found on GitHub")
            return -1
    elif args.subparsers == 'remove':
        pass

    return 0


if __name__ == '__main__':
    sys.exit(main())