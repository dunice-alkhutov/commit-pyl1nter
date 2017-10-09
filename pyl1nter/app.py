#!/usr/bin/python

"""
Pre-commit linter
"""

import sys
from pyl1nter.utils import run


def main(argv):
    """
    Main func
    """
    print('Starting checking you code...')
    run(argv)
    sys.exit(1)
