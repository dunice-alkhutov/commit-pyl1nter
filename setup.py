"""
commit-pyl1nt
-------------
Python pre-commit tool to check you code against some of the style conventions
in PEP 8 and check complexity of your clasees and functions.
"""
from setuptools import setup

setup(
    name='commit-pyl1nt',
    version='1.0.4',
    url='https://github.com/dunice-alkhutov/commit-pyl1nter',
    license='GNU',
    author='Alexey Alkhutov',
    author_email='a.alkhutov@dunice.net',
    description='Pacakge Description',
    long_description=__doc__,
    packages=['pyl1nter'],
    scripts=['bin/pyl1nter'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'pycodestyle',
        'pylint',
        'radon',
    ],
    download_url='https://github.com/dunice-alkhutov/commit-pyl1nter/tarball/1.0',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: Other/Proprietary License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
