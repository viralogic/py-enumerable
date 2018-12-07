import os
from setuptools import setup, find_packages


def read(*paths):
    """
    Build a file path from * paths and return the contents
    :param paths:
    :return:
    """
    with open(os.path.join(*paths), 'r') as f:
        return f.read()

setup(
    name='py-linq',
    version='0.6.0',
    description='Linq for Python. Now supports Python 3',
    long_description=(read('README.md') + '\n\n' + read('HISTORY.md') + '\n\n' + read('AUTHORS.md') + '\n\n' + read('CONTRIBUTING.md')),
    url='https://github.com/viralogic/py-enumerable',
    license='MIT',
    author='Bruce Fenske',
    author_email='bwfenske@ualberta.ca',
    packages=find_packages(exclude=['tests*']),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]


)
