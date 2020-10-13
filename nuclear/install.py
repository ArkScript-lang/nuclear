# coding: utf-8

import argparse
import requests
import hashlib

from os import makedirs

from .utils import (
    get,
    log,
    lockfile,
    package,
    get_dir,
)

def install_all() -> int:
    package_dict = lockfile.parse_lockfile()
    if not package_dict:
        print('no packages to be installed')
        return 0

    for package_name,package_info in package_dict.items():
        version = package_info[1]
        print(f"installing {package_name} with version {version}")
        install_single_package(package_info[0], package_info[1])

    return 0

def handle(args: argparse.Namespace) -> int:
    # check if any argument passed
    if args.package:
        return install_single_package(args.package,args.version)
    else:
        return install_all()

def install_single_package(package_name:str, version:str) -> int:
    # check for validity
    if not package.is_valid_package_name(package_name):
        log.error(f"Provided package name is not valid: {package_name}")
        return -1

    # then check for existance on GitHub
    user, repo = package_name.split('/')

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

    tar_addr, used_version = get.search_tar(user, repo, version)
    # error handling for when tar_addr is None has already been done
    if tar_addr is not None:
        # download
        r = requests.get(tar_addr)
        # get filename from content-dispositon
        filename = get_dir.get_filename(r.headers.get('content-disposition'))
        #try making the tarball
        try:  
            makedirs(get_dir.get_dir_name(tar_addr,version=version), exist_ok=True)
            with open(get_dir.get_dir_name(tar_addr,version=version)+"/"+filename,'wb',) as f:
                f.write(r.content)
            sha256 = hashlib.sha256(r.content).hexdigest()
            lockfile.save(user, repo, used_version, tar_addr, sha256)
        except Exception as e:
            log.error(f"{e}")
            print("Unable to download module")
    return 0
