# Paxter

<table>
    <tbody>
        <tr class="odd">
            <td>docs</td>
            <td>
                <a href="https://readthedocs.org/projects/paxter"><img src="https://readthedocs.org/projects/paxter/badge/?style=flat" alt="Documentation Status" /></a>
            </td>
        </tr>
        <tr class="even">
            <td>tests</td>
            <td>
                <div class="line-block">
                    <a href="https://travis-ci.org/abhabongse/paxter"><img src="https://api.travis-ci.org/abhabongse/paxter.svg?branch=master" alt="Travis-CI Build Status" /></a>
                    <a href="https://requires.io/github/abhabongse/paxter/requirements/?branch=master"><img src="https://requires.io/github/abhabongse/paxter/requirements.svg?branch=master" alt="Requirements Status" /></a>
                    <br />
                    <a href="https://codecov.io/github/abhabongse/paxter"><img src="https://codecov.io/github/abhabongse/paxter/coverage.svg?branch=master" alt="Coverage Status" /></a>
                    <br />
                    <a href="https://www.codacy.com/app/abhabongse/paxter"><img src="https://img.shields.io/codacy/grade/0d0c904fe452419692107d3163fe49b5.svg" alt="Codacy Code Quality Status" /></a>
                </div>
            </td>
        </tr>
        <tr class="odd">
            <td>package</td>
            <td>
                <div class="line-block">
                    <a href="https://pypi.org/project/paxter"><img src="https://img.shields.io/pypi/v/paxter.svg" alt="PyPI Package latest release" /></a>
                    <a href="https://pypi.org/project/paxter"><img src="https://img.shields.io/pypi/wheel/paxter.svg" alt="PyPI Wheel" /></a>
                    <a href="https://pypi.org/project/paxter"><img src="https://img.shields.io/pypi/pyversions/paxter.svg" alt="Supported versions" /></a>
                    <a href="https://pypi.org/project/paxter"><img src="https://img.shields.io/pypi/implementation/paxter.svg" alt="Supported implementations" /></a>
                    <br />
                    <a href="https://github.com/abhabongse/paxter/compare/v0.1.0...master"><img src="https://img.shields.io/github/commits-since/abhabongse/paxter/v0.1.0.svg" alt="Commits since latest release" /></a>
                </div>
            </td>
        </tr>
    </tbody>
</table>

Document-first text pre-processing mini-language, _loosely_ inspired by [at-expressions in Racket](https://docs.racket-lang.org/scribble/reader.html).

This is still a **work in progress** and a lot stuff are **subjected to change**.


## Installation

    pip install paxter

You can also install the in-development version with:

    pip install https://github.com/abhabongse/paxter/archive/master.zip

## Documentation

- [See rough description of grammar here.](paxter/core/__init__.py)
- <https://paxter.readthedocs.io/>

## Development

To run the all tests run:

    tox

Note, to combine the coverage data from all the tox environments run:

<table>
    <colgroup>
        <col style="width: 10%" />
        <col style="width: 90%" />
    </colgroup>
    <tbody>
        <tr class="odd">
            <td>Windows</td>
            <td><pre><code>set PYTEST_ADDOPTS=--cov-append
tox</code></pre></td>
        </tr>
        <tr class="even">
            <td>Other</td>
            <td><pre><code>PYTEST_ADDOPTS=--cov-append tox</code></pre></td>
        </tr>
    </tbody>
</table>
