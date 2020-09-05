# coding: utf-8

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