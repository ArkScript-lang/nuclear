# coding: utf-8

import requests
import json


def check_user(username: str) -> bool:
    """
    Check if a user exists on Github, by it's username
    """
    r = requests.get(f"https://api.github.com/users/{username}")
    return r.status_code == 200


def check_repo(username: str, repo: str) -> bool:
    """
    Check if a repository is owned by a given user on GitHub
    """
    r = requests.get(f"https://api.github.com/repos/{username}/{repo}")
    return r.status_code == 200