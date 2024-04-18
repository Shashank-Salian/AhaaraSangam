from random import randint

from .raw_data import QUOTES


def get_random_quotes():
    return QUOTES[randint(0, len(QUOTES) - 1)]
