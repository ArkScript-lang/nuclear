# coding: utf-8

import colorama


def error(message: str):
    print(colorama.Fore.RED + message + colorama.Fore.RESET)