# Paxter

<table>
    <tbody>
        <tr class="odd">
            <td><b>Docs</b></td>
            <td>
                <a href="https://readthedocs.org/projects/paxter"><img src="https://readthedocs.org/projects/paxter/badge/?style=flat" alt="Documentation Status" /></a>
            </td>
        </tr>
        <tr class="even">
            <td><b>Tests</b></td>
            <td>
                <div class="line-block">
                    <a href="https://travis-ci.com/abhabongse/paxter"><img src="https://api.travis-ci.com/abhabongse/paxter.svg?branch=master" alt="Travis-CI Build Status" /></a>
                    <a href="https://requires.io/github/abhabongse/paxter/requirements/?branch=master"><img src="https://requires.io/github/abhabongse/paxter/requirements.svg?branch=master" alt="Requirements Status" /></a>
                    <a href="https://codecov.io/github/abhabongse/paxter"><img src="https://codecov.io/github/abhabongse/paxter/coverage.svg?branch=master" alt="Coverage Status" /></a>
                    <a href="https://www.codacy.com/app/abhabongse/paxter"><img src="https://img.shields.io/codacy/grade/0d0c904fe452419692107d3163fe49b5.svg" alt="Codacy Code Quality Status" /></a>
                </div>
            </td>
        </tr>
        <tr class="odd">
            <td><b>Package</b></td>
            <td>
                <div class="line-block">
                    <a href="https://pypi.org/project/paxter"><img src="https://img.shields.io/pypi/v/paxter.svg" alt="PyPI Package latest release" /></a>
                    <a href="https://pypi.org/project/paxter"><img src="https://img.shields.io/pypi/wheel/paxter.svg" alt="PyPI Wheel" /></a>
                    <a href="https://pypi.org/project/paxter"><img src="https://img.shields.io/pypi/pyversions/paxter.svg" alt="Supported versions" /></a>
                    <a href="https://pypi.org/project/paxter"><img src="https://img.shields.io/pypi/implementation/paxter.svg" alt="Supported implementations" /></a>
                </div>
            </td>
        </tr>
    </tbody>
</table>

Document-first text pre-processing mini-language, _loosely_ inspired by [at-expressions in Racket](https://docs.racket-lang.org/scribble/reader.html).

**Warning:** This is still a _work in progress_ and a lot stuff are _subjected to change_.

## Installation

This package can be installed from PyPI via `pip` command
(or any other methods of your choice):

```shell script
$ pip install paxter
```

## Programmatic Usage

The package is intended to be used as a library.
Standard transformers are available to be utilized right away
without having to write custom parsed tree transformers.

Here is one way to use this library.

```python
from paxter.core import Parser, SimplePythonTransformer

parser = Parser()
transformer = SimplePythonTransformer()

env = {
    'name': "John Smith",
    'age_last_year': 47,
    'strip': lambda token: token.strip(),
    'tag': lambda token, label: f"<{label}>{token}</{label}>",
}

tree = parser.parse('''\
@!##{
def add_one(num):
    return num + 1
}##

Hello, my @strip{  full name   } is @name.
@tag[label="b"]{@name is @{age_last_year + 1} years old.}
@!{age_this_year = age_last_year + 1}

Do you know that 1 + 1 = @{1 + 1}?
''')

updated_env, output_text = transformer.transform(env, tree)
print(f"Age this year: {updated_env['age_this_year']}")
print(output_text)
```

The above script will print the following text:

```text
Age this year: 48


Hello, my full name is John Smith.
<b>John Smith is 48 years old.</b>


Do you know that 1 + 1 = 2?
```

Library users could also write their own custom transformers
by extending the `paxter.core.BaseTransformer` class
and use it in any way they want. Stay tuned for the tutorial.

## CLI Usage

While this feature is not ready,
users can try make a call to the following command:

```shell script
$ python -m paxter  # provide --help for help messages
```

## Documentation

-   [Rough description of Paxter grammar](src/paxter/core/__init__.py)
-   [ReadTheDocs documentation](https://paxter.readthedocs.io/) (under construction)

## Future Plans

-   Experiment with different kinds of transformers and use it in real life
-   Richer experience with environments and stores 
    (adding standard string functions, etc.)
-   Re-implementing lexers and parsers in Rust for better performance
    and portability to other environments (such as WASM). 
-   And more!

## Development

`Makefile` contains a lot of utility scripts.  
See help command by simply running `make` or `make help`.
