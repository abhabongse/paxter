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

Paxter is a document-first text pre-processing mini-language, _loosely_ inspired by
[at-expressions in Racket](https://docs.racket-lang.org/scribble/reader.html).  

-   The language mainly provides a way to parse an input text into a document tree
([similarly to a DOM](https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model/Introduction)).
-   The language itself **does not specify** how the parsed tree will be transformed
into the final rendered output text.
-   Users of this package may opt-in to use pre-defined _flavors_ of tree transformers
or choose to implement a new one by themselves. 

## Installation

This package can be installed from PyPI via `pip` command
(or any other methods of your choice):

```shell script
$ pip install paxter
```

## Programmatic Usage

The package is _mainly_ intended to be used as a library.
Pre-defined tree transformers are available to be utilized right away
without users having to write custom transformers.

Here is one way to use this library with **Simple Snake** flavor of tree transformer:

```python
from paxter.legacy import Parser
from paxter.flavors import SimpleSnakeTransformer

parser = Parser()
transformer = SimpleSnakeTransformer()

env = {
    'name': "John Smith",
    'age': 47,
    'occupation': "Student",
    'strip': lambda token: token.strip(),
    'tag': lambda token, label: f"<{label}>{token}</{label}>",
}

tree = parser.parse('''\
@!##{
def add_one(num):
    return num + 1
}##\
\
@strip{   Hello, my full name is @tag[label="b"]{John Smith}   }.
I am currently @age years old, and by this time next year I will be @{age + 1} years old.
My email is @"john@example.com".
@!{age_next_year = add_one(age)}\

Do you know that 1 + 1 = @{1 + 1}?

@!##{
import itertools

counter = itertools.count(start=1)
}##\
\
Let's count: @{next(counter)}, @{next(counter)}, @{next(counter)}.
''')

updated_env, output_text = transformer.transform(env, tree)
print(f"Age next year: {updated_env['age_next_year']}")
print(output_text)
```

The above script will print the following text:

```text
Age next year: 48
Hello, my full name is <b>John Smith</b>.
I am currently 47 years old, and by this time next year I will be 48 years old.
My email is john@example.com.

Do you know that 1 + 1 = 2?

Let's count: 1, 2, 3.
```

Library users could also write their own custom transformers
by extending the `paxter.core.BaseTransformer` class
and use it in any way they want. Stay tuned for the tutorial.

## CLI Usage

While this feature is still a work in progress,
users may try making a call to the following command to get started:

```shell script
$ python -m paxter  # provide --help for help messages
```

## Documentation

-   [Rough description of Paxter grammar](src/paxter/legacy/__init__.py)
-   [ReadTheDocs documentation](https://paxter.readthedocs.io/) (under construction)
-   Paxter documentation can be generated with [`pdoc3`](https://pdoc3.github.io/pdoc/) which can be installed with `pip install pdoc3`. Then preview this package with `pdoc --html : paxter` or compiled with `pdoc --html paxter`.

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
