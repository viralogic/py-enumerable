![Python package](https://github.com/viralogic/py-enumerable/workflows/Python%20package/badge.svg)

# py-linq #

LINQ (Language Integrated Query) is a popular querying language available in .NET. This library ports the language so
that developers can query collections of objects using the same syntax. This library would be useful for Python developers
with experience using the expressiveness and power of LINQ.

## Install ##

Available as a package from PyPI.

```bash
pip install py-linq
```

## Usage

To access the LINQ functions an iterable needs to be wrapped by the Enumerable

```python
from py_linq import Enumerable
my_collection = Enumerable([1, 2, 3])
```

## Documentation ##

Please visit the project [site](https://viralogic.github.io/py-enumerable) for better documentation

## Contributing ##

Contributions are welcomed. This project uses [poetry](https://python-poetry.org/docs/) to handle the few library dependencies. [Pre-commit](https://pre-commit.com/) is also used so that formatting and linting checks are performed on commit.

1. Clone the repository using `git clone https://github.com/viralogic/py-enumerable.git`
2. Install poetry globally as per the instructions [here](https://python-poetry.org/docs/)
3. CD into the root of your cloned repository directory and `poetry install` to install all packages from the repository Pipfile.
4. Install `pre-commit` by typing `poetry run pre-commit install`
5. You should now be ready to start coding!



