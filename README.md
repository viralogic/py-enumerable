![Python package](https://github.com/viralogic/py-enumerable/workflows/Python%20package/badge.svg)

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

## Contributing ##

Contributions are welcomed. This project uses [pipenv](https://pipenv-fork.readthedocs.io/en/latest/) to handle the few library dependencies. [Pre-commit](https://pre-commit.com/) is also used so that formatting and linting checks are performed on commit.

1. Clone the repository using `git clone https://github.com/viralogic/py-enumerable.git`
2. Install pipenv globally `pip install pipenv`
3. CD into the root of your cloned repository directory and `pipenv install --dev` to install all packages from the repository Pipfile.
4. Install `pre-commit` by typing `pipenv run pre-commit install`
5. You should now be ready to start coding!

## Authors ##

[Bruce Fenske](https://github.com/viralogic)

## Contributors ##

1. [Oleg Shilo](https://github.com/oleg-shilo)
2. [Sebastien Celles](https://github.com/scls19fr)
3. [Daniel Goltz](https://github.com/dagoltz)

## History ##

<table>
    <thead>
        <tr>
            <th>Date</th>
            <th style='text-align: right;'>Version</th>
            <td>Description</td>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>21-Apr-2020</td>
            <td style='text-align: right;'>1.2.2</td>
            <td>
                <ul>
                    <li>Issue #38 - Fixed issue where to_list calls were taking a very long time. Added some regression testing for this issue</li>
                    <li>General performance improvements across code-base where identified</li>
                </ul>
            </td>
        </tr>
        <tr>
            <td>21-Jan-2020</td>
            <td style='text-align: right;'>1.2.1</td>
            <td>
                <ul>
                    <li>Issue #36 - Fixed iterating over files</li>
                </ul>
            </td>
        </tr>
        <tr>
            <td>24-Nov-2019</td>
            <td style='text-align: right;'>1.2.0</td>
            <td>
                <ul>
                    <li>Memory consumption improvements by removal of data caching when collection is iterated over</li>
                    <li>Issue #22 - Unexpected behaviour when using iterator as input data</li>
                    <li>Issue #34 - Data loss when using any function</li>
                    <li>Issue #35 - Unexpected result when using first function<li>
                </ul>
            </td>
        </tr>
        <tr>
            <td>7-Oct-2019</td>
            <td style='text-align: right;'>1.1.0</td>
            <td>
                <ul>
                    <li>Issue #23 - Any accepts a None predicate</li>
                    <li>Issue #24 - Performance improvement where any returns on first matching element</li>
                    <li>Issue #25 - Use of any to check for elements in an Enumerable</li>
                    <li>Issue #26 - Performance improvement where element_at only iterates until the n-th element</li>
                    <li>Issue #29 - Performance improvement where distinct method is no longer immediately executing.</li>
                    <li>Issue #30 - Performance improvement where all function is no longer iterating through collection more than once</li>
                    <li>Issue #31 - Performance improvement where reverse function is no longer immediately executing</li>
                    <li>Issue #32 - Count function now accepts a lambda predicate to filter collection</li>
                </ul>
            </td>
        </tr>
        <tr>
            <td>16-Jul-2019</td>
            <td style='text-align: right;'>1.0.1</td>
            <td>
                <ul>
                    <li>Issue #21 - Support lambda predicates in first, first_or_default, last, and last_or_default methods</li>
                </ul>
            </td>
        </tr>
        <tr>
            <td>07-Mar-2019</td>
            <td style='text-align: right;'>1.0</td>
            <td>
                <ul>
                    <li>Issue #17 - Added additional LINQ methods to complete the <code>Enumerable</code> API as per <a href="https://docs.microsoft.com/en-us/dotnet/api/system.linq.enumerable?view=netframework-4.7.2">MSDN</a></li>
                </ul>
            </td>
        </tr>
        <tr>
            <td>06-Jan-2019</td>
            <td style='text-align: right;'>0.7</td>
            <td>
                <ul>
                    <li>Issue #19 - Distinct bug fix</li>
                </ul>
            </td>
        </tr>
        <tr>
            <td>06-Dec-2018</td>
            <td  style='text-align: right;'>0.6</td>
            <td>
                <ul>
                    <li>Issue #13 - Empty list as default parameter</li>
                    <li>Issue #14 - except_ method bug fix</li>
                </ul>
            </td>
        </tr>
        <tr>
            <td>19-Jul-2017</td>
            <td style='text-align: right;'>0.5</td>
            <td>
                <ul>
                    <li>last and last_or_default method bug fixes</li>
                    <li>then_by and then_by_descending implementation</li>
                </ul>
            </td>
        </tr>
        <tr>
            <td>30-Jan-2017</td>
            <td style='text-align: right;'>0.4</td>
            <td>
                <ul>
                    <li>Added Python 3 support</li>
                </ul>
            </td>
        </tr>
        <tr>
            <td>15-Jan-2015</td>
            <td style='text-align: right;'>0.3</td>
            <td>
                <ul>
                    <li>Changed README.rst</li>
                    <li>Performance improvements</li>
                </ul>
            </td>
        </tr>
        <tr>
            <td>12-Jan-2015</td>
            <td  style='text-align: right;'>0.2</td>
            <td>
                <ul>
                    <li>Added documentation</li>
                </ul>
            </td>
        </tr>
        <tr>
            <td>07-Jan-2015</td>
            <td  style='text-align: right;'>0.1</td>
            <td>
                <ul>
                    <li>Initial beta release</li>
                </ul>
            </td>
        </tr>
    </tbody>
</table>
