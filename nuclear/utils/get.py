# coding: utf-8

import requests
from decouple import config

from . import log
from .errors import RatelimitError


def get(url: str, username: str='', token: str='') -> requests.Request:
    # save credentials temporarily
    # commented out for a while
    # if username or token:
    #     get.username = username
    #     get.token = token
    #     return
    if not token:
        token = config("GITHUB_ACCESS_TOKEN") # try to load from .env if possible
    if token:
        r = requests.get(url, headers={"Authorization":f"token {token}"})
    else:
        r = requests.get(url)

    if r.status_code == 403 and r.headers['X-Ratelimit-Remaining'] == '0':
        reset = requests.get('https://api.github.com/rate_limit')
        reset = int(reset.json()['rate']['reset']) if reset.status_code == 200 else None
        raise RatelimitError(r.json()['message'], reset)
    return r


def check_user(username: str) -> bool:
    """
    Check if a user exists on Github, by it's username
    """
    r = get(f"https://api.github.com/users/{username}")
    return r.status_code == 200


def check_repo(username: str, repo: str) -> bool:
    """
    Check if a repository is owned by a given user on GitHub
    """
    r = get(f"https://api.github.com/repos/{username}/{repo}")
    return r.status_code == 200

def get_latest_commit(username: str, repo: str) -> None or str:
    """
    Returns latest commit from a package
    """
    if version:
        return version
    r = get(f"https://api.github.com/repos/{username}/{repo}/commits/master")
    if r.status_code != 200:
        log.error(f"Couldn't retrieve latest commit from {username}/{repo}")
        return None
    return r.json()["sha"]


def search_tar(username: str, repo: str, version: str=None) -> list:
    """
    Search a specific release from a given GitHub repository
    If version is None, the latest release will be downloaded

    Returns None if the tar can not be downloaded (version can not be found)
    Otherwise, returns the address of the tarball
    """
    r = get(f"https://api.github.com/repos/{username}/{repo}/releases")
    if r.status_code != 200:
        log.error(f"Couldn't retrieve releases list from {username}/{repo}")
        return None, None
    releases = r.json()

    # no specified version, try to grab the latest version
    if version is None:
        # no release, just download the tar from the repo
        # but add a warning
        if len(releases) == 0:
            log.warn(f"Downloading the latest tarball from {username}/{repo} since no release were available")
            return f"https://api.github.com/repos/{username}/{repo}/tarball", get_latest_commit(username, repo)
        else:
            log.info(f"Downloading version {releases[0]['tag_name']} from {username}/{repo}")
            return releases[0]['tarball_url'], releases[0]['tag_name']
    # the given version isn't known to github
    elif not any(e['tag_name'] == version for e in releases):
        log.error(f"Requested version {version} for {username}/{repo} can not be found, aborting")
        versions = ', '.join(e['tag_name'] for e in releases)
        if versions:
            log.info(f"Available versions are {versions}")
        else:
            log.warn(
                "There are no available releases, try without specifying " + \
                "one to download the package at its current commit stage"
            )
        return None, None
    else:
        # search for the wanted release and return its tarbar url
        # it *must* exists since the previous elif has failed if
        # we're here.
        for rel in releases:
            if rel['tag_name'] == version:
                return rel['tarball_url'], rel['tag_name']