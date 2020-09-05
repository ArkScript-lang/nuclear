# coding: utf-8

import os
import sys
from typing import List


def main(*args: List[str]) -> int:
    """
    The main function of the program
    """
    print(*args)
    return 0


if __name__ == '__main__':
    sys.exit(main(*sys.argv[1:]))