"""
Helping functions and inner logic
"""


from subprocess import PIPE
import pycodestyle
import inspect
from pylint import epylint as lint
from radon.complexity import cc_visit
from radon.visitors import (Class as radon_class,
                            Function as radon_func)


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


def check_complexity(filepath):
    """
    Check file with radon lib and get complexity of his classes and functions
    """
    with open(filepath, 'r') as _file:
        results = cc_visit(_file.read())
        reports = []
        for result in results:
            if result.complexity > 10: # 5 is temp value. 10 is correct
                file_report = dict(
                    file=filepath,
                    complexity=result.complexity,
                    message=get_complexity_message(result.complexity),
                    line_number=result.lineno,
                    object_name=result.name
                )
                if isinstance(result, radon_class):
                    file_report['type'] = 'class'
                if isinstance(result, radon_func):
                    file_report['type'] = 'function'
                reports.append(file_report)
    return reports


def get_complexity_message(complexity):
    """
    Get complexity (int type) and return message
    """
    if complexity > 40:
        return "Very high risk - error-prone, unstable block"
    elif complexity > 30:
        return "High risk - complex block, alarming"
    elif complexity > 20:
        return "More than moderate risk - more complex block"
    elif complexity < 10:
        return "Low risk - well structured and stable block"
    else:
        return "Moderate risk - slightly complex block"



def lint_files(files):
    """
    Lint modified files and create report
    or commit changes with message.
    """
    pep8 = 12 # for debugging

    filtered_files = filter_files(files)
    lint_results = []
    complexity_results = []
    for _file in filtered_files:
        if pep8 == 1:
            fchecker = pycodestyle.Checker(_file, show_source=True)
            file_errors = fchecker.check_all()
        elif pep8 == 0:
            stdout, stderr = lint.py_run(_file, return_std=True)
            # HINT! stdout.read() does not equal True
            # when is put within 'if' condition
            message = stdout.read() + ''
            if message:
                print('Error:', message)

        complexity_results += check_complexity(_file)

    show_results(lint_results, complexity_results)


def show_results(lint_results, complexity_results):
    """
    Show result of package working
    """
    if not len(lint_results) and not len(complexity_results):
        print("Mother of GOD... Your code is nice!")
        return make_commit()
    for l_result in lint_results:
        print('Lint:', l_result)

    for c_result in complexity_results:
        print('********************')
        print('File: {}, line: {}, {} {}'.format(c_result['file'],
                                                 c_result['line_number'],
                                                 c_result['type'],
                                                 c_result['object_name']))
        print('Complexity: {}'.format(c_result['complexity']))
        print('Comment: {}'.format(c_result['message']))


def has_error(message):
    print('m[0]:', message[0])
    return not message.startswith(' ----')


def filter_files(files):
    """
    Filter files for *.py files only
    """
    return [_file for _file in files if _file.endswith('.py')]
