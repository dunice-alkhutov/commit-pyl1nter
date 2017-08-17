"""
Commit linter
"""

import sys
from utils import run


def main(argv):
    """
    Main func
    """
    print('Starting checking you code...')
    run(argv)


if __name__ == '__main__':
    main(sys.argv[1:])
