#!/usr/bin/python

"""
Pre-commit linter
"""

import sys
from utils import run


def main(argv):
    """
    Main func
    """
    print('Starting checking you code...')
    run(argv)
    sys.exit(1)


if __name__ == '__main__':
    main(sys.argv[1:])
