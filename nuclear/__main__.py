# coding: utf-8

import os
import sys
import argparse
from typing import List
import colorama
import time

from .install import handle as install_handler
from .remove import handle as remove_handler
from .utils.errors import RatelimitError
from .utils import log
from .utils import get


def main() -> int:
    """
    The main function of the program
    """
    colorama.init()

    parser = argparse.ArgumentParser(prog='nuclear', add_help=True)
    auth_group = parser.add_argument_group(
        title='Authentication',
        description='This section is optional but giving GitHub personal token can help' + \
            ' to raise the rate limit errors (60 request/hour at most)\n' +
            ' Your credentials (personal access token) will be saved to the disk in a' + \
            ' .env file.\n' + \
            ' If you are in a git repo (.git is present in the current' + \
            ' folder, or .gitignore is present in the current folder),' + \
            ' then it will automatically be added to the file (.gitignore will be' + \
            ' created if it doesn\'t exist) to avoid credentials leaking.'

    )
    auth_group.add_argument('--login', help='GitHub login, optional')
    auth_group.add_argument('--token', help='GitHub token, required if rate limiting is an issue')
    subparsers = parser.add_subparsers(dest='subparsers')

    # install package [-v version]
    install = subparsers.add_parser(
        'install', help='Install an ArkScript package from GitHub'
    )
    install.add_argument('--package', help='Should look like this: user/repo')
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

    if args.login:
        if not args.token:
            log.error('GitHub login provided but token wasn\'t given')
            return -1
        else:
            # save credentials
            with open('.env', 'w') as f:
                f.write(f"GITHUB_ACCESS_TOKEN={args.token}")
            # NOT REQUIRED NOW, SINCE GET IS CONFIGURED
            # TO READ DRECTLY FROM ENV FILE IF TOKEN EXISTS
            # -------------------------------------------
            # register into get
            # get.get('', args.login, args.token)
            # check for .gitignore and add our file to it
            # in order to prevent token leaking
            # --------------------------------------------
            if os.path.exists('.gitignore') or os.path.exists('.git'):
                with open('.gitignore', 'a+') as file:
                    file.seek(0) # to read actual contents first
                    contents = file.readlines()
                    if ".env\n" not in contents and ".env" not in contents:
                        file.write('.env')
        # REMOVED BECAUSE ARGS.LOGIN NOT NEEDED
        # -----------------------------------------------
        # else:
        #     # check for .nuclear.github file
        #     if os.path.exists('.nuclear.github'):
        #         with open('.nuclear.github') as file:
        #             get.get('', *file.readlines())
        # -----------------------------------------------

    try:
        if args.subparsers == 'install':
            return install_handler(args)
        elif args.subparsers == 'remove':
            return remove_handler(args)
    except RatelimitError as rle:
        log.error(rle.message)
        if rle.reset is not None:
            reset = time.strftime("%H:%M:%S %D", time.localtime(rle.reset))
            log.info(f"Will reset at {reset}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
