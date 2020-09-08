# coding: utf-8


class RatelimitError(Exception):
    def __init__(self, message, reset):
        super().__init__()
        self.message = message
        self.reset = reset