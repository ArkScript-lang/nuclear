# coding: utf-8

import argparse
import requests
from os import makedirs

from .utils import (
    get,
    log,
    package,
    get_dir,
)


def handle(args: argparse.Namespace) -> int:
    # check for validity
    if not package.is_valid_package_name(args.package):
        log.error(f"Provided package name is not valid: {args.package}")
        return -1

    # then check for existance on GitHub
    user, repo = args.package.split('/')

    # first the user
    if not get.check_user(user):
        log.error(f"The GitHub user '{user}' doesn't exists")
        return -1
    # then the repo
    # we could've just check the repo but checking for the user first
    # can help identify why we can't install a package
    if not get.check_repo(user, repo):
        log.error(f"The wanted package '{repo}' from {user} couldn't be found on GitHub")
        return -1

    tar_addr = get.search_tar(user, repo, args.version)
    # error handling for when tar_addr is None has already been done
    if tar_addr is not None:
        # download
        r = requests.get(tar_addr)
        # get filename from content-dispoisiton
        filename = get_dir.get_filename(r.headers.get('content-disposition'))
        try:  
            makedirs(get_dir.get_dir_name(tar_addr))
            open(get_dir.get_dir_name(tar_addr)+"/"+filename,'xb').write(r.content)
        except Exception as e:
            log.error(f"{e}")
            print("Unable to download module")
    return 0