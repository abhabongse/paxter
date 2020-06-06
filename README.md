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
    Users have all the freedom to interpret or render the document tree into an output format however they like.
-   Instead of implementing a document tree renderer by themselves, users may opt-in to use pre-defined _flavors_ of document tree renderers also provided by this package. 


## Example

Let the input text be the following.

```text
@python##"
    import statistics
    from datetime import datetime

    _symbols_ = {
        '@': '@',
        '.': '&hairsp;',
        ',': '&thinsp;',
    }
    name = "Ashley"
    birth_year = 1987
    age = datetime.now().year - birth_year
"##\
My name is @name and I am @age years old.
My email is ashley@@example.com.
My shop opens Monday@,-@,Friday.

@python##"
    from itertools import count
    counter = count(start=1)
"##\
Counting is as easy as @|next(counter)|, @|next(counter)|, @|next(counter)|.
Arithmetic? Not a problem: 7 * 11 * 13 = @|7 * 11 * 13|.

Escaping is easy, just enclose the text with as many #...# as you like.
For example, one way to escape the @#""@""# symbol, you can write @##"@#""@""#"##.
In turn, to write @##"@#""@""#"## as-is, you can do by typing @###"@##"@#""@""#"##"###.

@python##"
    def is_odd(value):
        return value % 2 == 1
"##\
Odd digits are@flatten{@for[i in @|range(10)|]{@if[@|is_odd(i)|]{ @i}}}.
Expected outcome for rolling a die is @|statistics.mean|[@|range(1, 7)|].
```

Suppose that we are using the Python authoring mode (which is an rendering extension of Paxter library package).
Then the above input text will render to the following output.

```text
My name is Ashley and I am 33 years old.
My email is ashley@example.com.
My shop opens Monday&thinsp;-&thinsp;Friday.

Counting is as easy as 1, 2, 3.
Arithmetic? Not a problem: 7 * 11 * 13 = 1001.

Escaping is easy, just enclose the text with as many #...# as you like.
For example, one way to escape the "@" symbol, you can write @#""@""#.
In turn, to write @#""@""# as-is, you can do by typing @##"@#""@""#"##.

Odd digits are 1 3 5 7 9.
Expected outcome for rolling a die is 3.5.
```


## Documentation

Information available at [ReadTheDocs documentation](https://paxter.readthedocs.io/) website:
 
-   [Installation and Getting Started](https://paxter.readthedocs.io/en/latest/getting_started.html)
-   [Paxter Language Tutorial](https://paxter.readthedocs.io/en/latest/paxter_language_tutorial.html)
-   [Python Authoring Mode Tutorial](https://paxter.readthedocs.io/en/latest/python_authoring_mode_tutorial.html)
-   [Custom Renderer Tutorial](https://paxter.readthedocs.io/en/latest/custom_renderer_tutorial.html)
-   [Syntax Reference](https://paxter.readthedocs.io/en/latest/syntax.html)
-   [Core API Reference](https://paxter.readthedocs.io/en/latest/core_api.html)
-   and more


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
