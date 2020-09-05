# coding: utf-8

import urllib.request as req
import json


def check_user(self, username: str) -> bool:
    """
    Check if a user exists on Github, by it's username
    """
    response = req.urlopen(f"https://api.github.com/users/{username}")
    data = response.read()
    content = json.loads(data.decode('utf-8'))

    # if the user doesn't exist, the API will add a field message
    # otherwise, there is a login field
    return content.get('message') is None and content.get('login') is not None


def check_repo(self, username: str, repo: str) -> bool:
    """
    Check if a repository is owned by a given user on GitHub
    """
    response = req.urlopen(f"https://api.github.com/repos/{username}/{repo}")
    data = response.read()
    content = json.loads(data.decode('utf-8'))

    # if the repository doesn't exist or is private, we won't be able to get it
    # thus we'll have a message: Not Found, and not a field name
    return content.get('message') is None and content.get('name') is not None