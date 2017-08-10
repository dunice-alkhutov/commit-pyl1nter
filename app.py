"""
Commit linter
"""

import subprocess
import pycodestyle

MODIFIED_FILE_TEXT = 'modified:'
NEW_FILE_TEXT = 'new file:'


def main():
    """
    Main func
    """

    bash_command = "git status"
    process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    print(f'error: {error}')
    ustaged_files = collect_files_from_commit(str(output, 'utf-8'))
    lint_files(ustaged_files)


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
        files.append(row[file_name_index + len(text):].strip())

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

    print('Files were  :', files)
    filtered_files = filter_files(files)
    print('Files bacame:', filtered_files)
    for _file in filtered_files:
        fchecker = pycodestyle.Checker(_file, show_source=True)
        file_errors = fchecker.check_all()
        print('file errs', file_errors)


def filter_files(files):
    """
    Filter files for *.py files only
    """

    return [_file for _file in files if _file.endswith('.py')]


if __name__ == '__main__':
    main()
