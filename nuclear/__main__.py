# coding: utf-8

import os
import sys


def main(*args):
    print(*args)
    return 0


if __name__ == '__main__':
    sys.exit(main(*sys.argv[1:]))