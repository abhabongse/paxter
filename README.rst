========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |requires|
        | |codecov|
        | |codacy|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|

.. |docs| image:: https://readthedocs.org/projects/paxter/badge/?style=flat
    :target: https://readthedocs.org/projects/paxter
    :alt: Documentation Status

.. |travis| image:: https://api.travis-ci.org/abhabongse/paxter.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/abhabongse/paxter

.. |requires| image:: https://requires.io/github/abhabongse/paxter/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/abhabongse/paxter/requirements/?branch=master

.. |codecov| image:: https://codecov.io/github/abhabongse/paxter/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/abhabongse/paxter

.. |codacy| image:: https://img.shields.io/codacy/grade/0d0c904fe452419692107d3163fe49b5.svg
    :target: https://www.codacy.com/app/abhabongse/paxter
    :alt: Codacy Code Quality Status

.. |version| image:: https://img.shields.io/pypi/v/paxter.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/paxter

.. |wheel| image:: https://img.shields.io/pypi/wheel/paxter.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/paxter

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/paxter.svg
    :alt: Supported versions
    :target: https://pypi.org/project/paxter

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/paxter.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/paxter

.. |commits-since| image:: https://img.shields.io/github/commits-since/abhabongse/paxter/v0.1.0.svg
    :alt: Commits since latest release
    :target: https://github.com/abhabongse/paxter/compare/v0.1.0...master



.. end-badges

Document-first text pre-processing mini-language loosely inspired by at-expressions in Racket

* Free software: Apache Software License 2.0

Installation
============

::

    pip install paxter

You can also install the in-development version with::

    pip install https://github.com/abhabongse/paxter/archive/master.zip


Documentation
=============


https://paxter.readthedocs.io/


Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
