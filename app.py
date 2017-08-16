"""
Commit linter
"""

import subprocess
from utils import collect_files_from_commit, lint_files


def main():
    """
    Main func
    """

    bash_command = "git status"
    process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    if error: print('Bash command error: {}'.format(error))

    ustaged_files = collect_files_from_commit(str(output, 'utf-8') )
    lint_files(ustaged_files)


if __name__ == '__main__':
    main()
