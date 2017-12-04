Python pre-commit tool to check you code against some of the style conventions in PEP 8 and check complexity of your clasees and functions
==========

Installation
-----------

Install lib to your virtualenv

```bash
pip install commit-pyl1nt
```

Quick start
-----------
Go to `/path_to_your_project/.git/hooks/`.
Create file `pre-commit` and fill it like this:
```bash
#!/bin/sh
pyl1nter -n 80
```

Make sure that `pre-commit` has execution rights

Do any changes in your project and try make a commit. 
This lib gets files list with changes by calling command `git status` and collect files to check. These will be only files with `.py` extensions.
You your code has inconsistencies with pep8 you will see in your console where they are. Also if some your classes and functuions have a high complex(large nesting, too many lines of code and etc) you will see message in console with descriptions.
In case if your code has any inconsistencies (with styles or complexity) the commit operation will be interrupted.
If you need to create commit anyway use flag `--no-verify`. E.g.:
```shell
$ git commit --no-verify -am "Commit message"
```