# coding: utf-8

import colorama


def error(message: str):
    print(colorama.Fore.RED + "[ERROR] " + message + colorama.Fore.RESET)


def warn(message: str):
    print(colorama.Fore.YELLOW + "[WARNING] " + message + colorama.Fore.RESET)


def info(message: str):
    print("[INFO] " + message)