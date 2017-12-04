"""
Helping functions and inner logic
"""


import sys
import getopt
import pycodestyle
from subprocess import Popen, PIPE
from pylint import epylint as lint
from radon.complexity import cc_visit
from radon.visitors import (Class as radon_class,
                            Function as radon_func)


MODIFIED_FILE_TEXT = 'modified:'
NEW_FILE_TEXT = 'new file:'
BASH_COMMAND = "git status"
MAX_LINE_LENGTH = 79


def run(argv):
    """
    Run all operations:
    - check git updated files
    - get script flags
    - start linter and complexity analize
    """
    process = Popen(BASH_COMMAND.split(), stdout=PIPE)
    output, error = process.communicate()
    if error:
        print('Bash command error: {}'.format(error))
        sys.exit(2)

    if sys.version < '3':
        ustaged_files = collect_files_from_commit(str(output))
    else:
        ustaged_files = collect_files_from_commit(str(output, 'utf-8'))
    linter, complex_val, output_file = check_flags(argv)
    lint_files(ustaged_files, linter, complex_val, output_file)


def check_flags(argv):
    """
    Handle scripts flags
    """
    linter = 'pep8'
    complex_val = 10
    output_file = None
    try:
        opts, _ = getopt.getopt(argv, "l:c:n: h", [])
    except getopt.GetoptError as ex:
        print("See help by 'python app.py -h'")
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            message = '''You can use next optional flags:
    -l  set linter. You can try 'pep8' or 'pylint'. Default is 'pep8'
        Setting another linter will raise exeption
    -c  Set lower complexity level. Default is 10
        Other values:
        1 - 5	A (low risk - simple block)
        6 - 10	B (low risk - well structured and stable block)
        11 - 20	C (moderate risk - slightly complex block)
        21 - 30	D (more than moderate risk - more complex block)
        31 - 40	E (high risk - complex block, alarming)
        41+	    F (very high risk - error-prone, unstable block)
    -n  Set maximum allowed line length. Default is 79
    Example: "pyl1nter -n 100 -c 15'''
    # -o  put statistics to output files
            print(message)
            sys.exit()

        if opt == '-l':
            linter = arg

        elif opt == '-c':
            try:
                complex_val = int(arg)
            except ValueError as ex:
                print('Wrong complexity value! Will be used default')
                complex_val = 10

        elif opt == '-o':
            output_file = arg

        elif opt == '-n':
            global MAX_LINE_LENGTH
            MAX_LINE_LENGTH = int(arg)

        else:
            sys.exit()

    return linter, complex_val, output_file


def collect_files_from_commit(text):
    """
    Parse result of 'git status' command and collect unstaged files
    """
    files_to_handle = []
    git_messages_rows = text.split('\n')

    def append_to_file(row, text):
        """
        Append new and not staged files to array
        """
        file_name_index = row.index(text)
        _file = row[file_name_index + len(text):].strip()
        if _file not in files_to_handle:
            files_to_handle.append(_file)

    for row in git_messages_rows:
        if MODIFIED_FILE_TEXT in row:
            append_to_file(row, MODIFIED_FILE_TEXT)

        if NEW_FILE_TEXT in row:
            append_to_file(row, NEW_FILE_TEXT)

    return files_to_handle


def check_complexity(filepath, complex_val=10):
    """
    Check file with radon lib and get complexity of his classes and functions
    """
    with open(filepath, 'r') as _file:
        results = cc_visit(_file.read())
        reports = []
        for result in results:
            if result.complexity > complex_val:
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

    return "Moderate risk - slightly complex block"


def lint_files(files, linter, complex_val, output_file=None):
    """
    Lint modified files and create report
    or commit changes with message.
    """
    filtered_files = filter_files(files)
    lint_results = []
    complexity_results = []

    for _file in filtered_files:
        if linter == 'pylint':
            stdout, stderr = lint.py_run(_file, return_std=True)

            # HINT! stdout.read() does not equal True
            # when is put within 'if' condition
            if stderr:
                print(stderr.read())
            message = stdout.read() + ''
            if has_error(message):
                lint_results.append(message)
                # print('Error:', message)

        else:
            if linter != 'pep8':
                print('Unknown linter. Will be used default')
                linter = 'pep8'

            fchecker = pycodestyle.Checker(_file,
                                           show_source=True,
                                           max_line_length=MAX_LINE_LENGTH)
            file_errors = fchecker.check_all()
            # print('file err', file_errors)
            if file_errors != 0:
                lint_results.append(file_errors)

        complexity_results += check_complexity(_file, complex_val)

    show_results(lint_results, complexity_results, output_file)


def write_result_to_file(output_file, text):
    """
    Write statistics to file
    """
    print('Write to {} text:\n{}'.format(output_file, text))
    print('But not today... :)')


def show_results(lint_results, complexity_results, output_file):
    """
    Show result of package working
    """
    if not lint_results and not complexity_results:
        print("Mother of GOD... Your code is nice!")
        sys.exit(0)

    for l_result in lint_results:
        print('Lint errors:', l_result)
        text = ''
        if (output_file):
            write_result_to_file(output_file, text)

    for c_result in complexity_results:
        text = '''********************
File: {}, line: {}, {}: {}
Complexity: {}
Comment: {}
'''.format(c_result['file'],
           c_result['line_number'],
           c_result['type'],
           c_result['object_name'],
           c_result['complexity'],
           c_result['message'])
        print(text)
        if (output_file):
            write_result_to_file(output_file, text)
    sys.exit(1)


def has_error(message):
    """
    If message starts with '*' sybmol
    """
    return message.startswith('*')


def filter_files(files):
    """
    Filter files for *.py files only
    """
    return [_file for _file in files if _file.endswith('.py')]
