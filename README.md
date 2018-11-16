[![](https://travis-ci.org/viralogic/py-enumerable.svg?branch=master)](https://travis-ci.org/viralogic/py-enumerable)

# py-linq #

LINQ (Language Integrated Query) is a popular querying language available in .NET. This library ports the language so
that developers can query collections of objects using the same syntax. This library would be useful for Python developers
with experience using the expressiveness and power of LINQ.

## Install ##

Available as a package from PyPI.

    pip install py-linq

## Usage

To access the LINQ functions an iterable needs to be wrapped by the Enumerable

    from py_linq import Enumerable
    my_collection = Enumerable([1,2,3])

## Documentation ##

Please visit the project [site](https://viralogic.github.io/py-enumerable) for better documentation