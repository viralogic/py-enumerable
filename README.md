[![](https://travis-ci.org/viralogic/py-enumerable.svg?branch=master)](https://travis-ci.org/viralogic/py-enumerable)
[![Coverage Status](https://coveralls.io/repos/github/viralogic/py-enumerable/badge.svg?branch=master)](https://coveralls.io/github/viralogic/py-enumerable?branch=master)

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

## Authors ##

[Bruce Fenske](https://github.com/viralogic)

## Contributors ##

1. [Oleg Shilo](https://github.com/oleg-shilo)
2. [Sebastien Celles](https://github.com/scls19fr)

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