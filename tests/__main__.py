# coding: utf-8

import sys
from typing import List
from nuclear import *


def main(*args: List[str]) -> int:
    """
    The main function of the tests
    """
    print(*args)
    return 0


if __name__ == '__main__':
    sys.exit(main(*sys.argv[1:]))