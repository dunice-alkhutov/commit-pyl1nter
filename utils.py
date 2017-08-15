"""
Helping functions and inner logic
"""


from subprocess import PIPE
import pycodestyle
from pylint import epylint as lint


MODIFIED_FILE_TEXT = 'modified:'
NEW_FILE_TEXT = 'new file:'


def make_commit():
    """
    Create commit
    """

    print('Make commit')


def collect_files_from_commit(text):
    """
    Parse result of 'git status' command and collect unstaged files
    """

    files = []
    rows = text.split('\n')

    def append_to_file(row, text):
        """
        Append new and not staged files to array
        """

        file_name_index = row.index(text)
        _file = row[file_name_index + len(text):].strip()
        if _file not in files:
            files.append(_file)

    for row in rows:
        if MODIFIED_FILE_TEXT in row:
            append_to_file(row, MODIFIED_FILE_TEXT)

        if NEW_FILE_TEXT in row:
            append_to_file(row, NEW_FILE_TEXT)

    return files


def lint_files(files):
    """
    Lint modified files and create report
    or commit changes with message.
    """

    pep8 = 1

    filtered_files = filter_files(files)
    for _file in filtered_files:
        print('FILE IS:', _file)
        if pep8:
            fchecker = pycodestyle.Checker(_file, show_source=True)
            file_errors = fchecker.check_all()
        else:
            stdout, stderr = lint.py_run(_file, return_std=True)
            # HINT! stdout.read() does not equal True
            # when is put within 'if' condition
            message = stdout.read() + ''
            if message:
                print('Error:', message)


def has_error(message):
    print('m[0]:', message[0])
    return not message.startswith(' ----')


def filter_files(files):
    """
    Filter files for *.py files only
    """

    return [_file for _file in files if _file.endswith('.py')]
