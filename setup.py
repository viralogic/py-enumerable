__author__ = 'Viralogic Software'

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
    version='0.1.0',
    description='Linq for Python',
    long_description=(read('README.rst') + '\n\n' + read('HISTORY.rst') + '\n\n' + read('AUTHORS.rst') + read('CONTRIBUTING.rst')),
    url='https://github.com/viralogic/py-enumerable',
    license='MIT',
    author='ViraLogic Software',
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
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]


)
