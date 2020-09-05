# coding: utf-8

import argparse

from .utils import get
from .utils import log
from .utils import package


def handle(args: argparse.Namespace) -> int:
    # check for validity
    if not package.is_valid_package_name(args.package):
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

    return 0