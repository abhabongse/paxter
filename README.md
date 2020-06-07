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

**Paxter** is a document-first, text pre-processing mini-language toolchain,
_loosely_ inspired by [@-expressions in Racket](https://docs.racket-lang.org/scribble/reader.html).

-   The Paxter library package mainly provides a toolchain for 
    parsing an input text (written in **Paxter language**) 
    into _an intermediate parsed tree_.
-   However, the Paxter toolchain **does not specify** how 
    the parsed tree should be interpreted or rendered into final result.
    Users of the Paxter library have all the freedom to do
    whatever they like to transform the intermediate result
    into a final output result they wish to achieve.  
-   Alternatively, instead of implementing an interpreter 
    for intermediate parsed tree by themselves,
    users may opt-in to utilize a preset _parsed tree renderers_,
    also provided by this library package.


## Example

Suppose that we have a text document written in Paxter language as shown below.

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

Using the parser in Paxter library package to process this document,
we obtain the following result.

```python
FragmentList(
    start_pos=0,
    end_pos=1031,
    children=[
        Command(
            start_pos=1,
            end_pos=248,
            intro="python",
            intro_enclosing=EnclosingPattern(left="", right=""),
            options=None,
            main_arg=Text(
                start_pos=10,
                end_pos=245,
                inner="\n    import statistics\n    from datetime import datetime\n\n    _symbols_ = {\n        '@': '@',\n        '.': '&hairsp;',\n        ',': '&thinsp;',\n    }\n    name = \"Ashley\"\n    birth_year = 1987\n    age = datetime.now().year - birth_year\n",
                enclosing=EnclosingPattern(left='##"', right='"##'),
                at_prefix=False,
            ),
        ),
        Text(
            start_pos=248,
            end_pos=261,
            inner="\\\nMy name is ",
            enclosing=EnclosingPattern(left="", right=""),
            at_prefix=False,
        ),
        Command(
            start_pos=262,
            end_pos=266,
            intro="name",
            intro_enclosing=EnclosingPattern(left="", right=""),
            options=None,
            main_arg=None,
        ),
        Text(
            start_pos=266,
            end_pos=276,
            inner=" and I am ",
            enclosing=EnclosingPattern(left="", right=""),
            at_prefix=False,
        ),
        Command(
            start_pos=277,
            end_pos=280,
            intro="age",
            intro_enclosing=EnclosingPattern(left="", right=""),
            options=None,
            main_arg=None,
        ),
        Text(
            start_pos=280,
            end_pos=310,
            inner=" years old.\nMy email is ashley",
            enclosing=EnclosingPattern(left="", right=""),
            at_prefix=False,
        ),
        Command(
            start_pos=311,
            end_pos=312,
            intro="@",
            intro_enclosing=EnclosingPattern(left="", right=""),
            options=None,
            main_arg=None,
        ),
        Text(
            start_pos=312,
            end_pos=345,
            inner="example.com.\nMy shop opens Monday",
            enclosing=EnclosingPattern(left="", right=""),
            at_prefix=False,
        ),
        Command(
            start_pos=346,
            end_pos=347,
            intro=",",
            intro_enclosing=EnclosingPattern(left="", right=""),
            options=None,
            main_arg=None,
        ),
        Text(
            start_pos=347,
            end_pos=348,
            inner="-",
            enclosing=EnclosingPattern(left="", right=""),
            at_prefix=False,
        ),
        Command(
            start_pos=349,
            end_pos=350,
            intro=",",
            intro_enclosing=EnclosingPattern(left="", right=""),
            options=None,
            main_arg=None,
        ),
        Text(
            start_pos=350,
            end_pos=359,
            inner="Friday.\n\n",
            enclosing=EnclosingPattern(left="", right=""),
            at_prefix=False,
        ),
        Command(
            start_pos=360,
            end_pos=434,
            intro="python",
            intro_enclosing=EnclosingPattern(left="", right=""),
            options=None,
            main_arg=Text(
                start_pos=369,
                end_pos=431,
                inner="\n    from itertools import count\n    counter = count(start=1)\n",
                enclosing=EnclosingPattern(left='##"', right='"##'),
                at_prefix=False,
            ),
        ),
        Text(
            start_pos=434,
            end_pos=459,
            inner="\\\nCounting is as easy as ",
            enclosing=EnclosingPattern(left="", right=""),
            at_prefix=False,
        ),
        Command(
            start_pos=460,
            end_pos=475,
            intro="next(counter)",
            intro_enclosing=EnclosingPattern(left="|", right="|"),
            options=None,
            main_arg=None,
        ),
        Text(
            start_pos=475,
            end_pos=477,
            inner=", ",
            enclosing=EnclosingPattern(left="", right=""),
            at_prefix=False,
        ),
        Command(
            start_pos=478,
            end_pos=493,
            intro="next(counter)",
            intro_enclosing=EnclosingPattern(left="|", right="|"),
            options=None,
            main_arg=None,
        ),
        Text(
            start_pos=493,
            end_pos=495,
            inner=", ",
            enclosing=EnclosingPattern(left="", right=""),
            at_prefix=False,
        ),
        Command(
            start_pos=496,
            end_pos=511,
            intro="next(counter)",
            intro_enclosing=EnclosingPattern(left="|", right="|"),
            options=None,
            main_arg=None,
        ),
        Text(
            start_pos=511,
            end_pos=554,
            inner=".\nArithmetic? Not a problem: 7 * 11 * 13 = ",
            enclosing=EnclosingPattern(left="", right=""),
            at_prefix=False,
        ),
        Command(
            start_pos=555,
            end_pos=568,
            intro="7 * 11 * 13",
            intro_enclosing=EnclosingPattern(left="|", right="|"),
            options=None,
            main_arg=None,
        ),
        Text(
            start_pos=568,
            end_pos=678,
            inner=".\n\nEscaping is easy, just enclose the text with as many #...# as you like.\nFor example, one way to escape the ",
            enclosing=EnclosingPattern(left="", right=""),
            at_prefix=False,
        ),
        Text(
            start_pos=681,
            end_pos=684,
            inner='"@"',
            enclosing=EnclosingPattern(left='#"', right='"#'),
            at_prefix=True,
        ),
        Text(
            start_pos=686,
            end_pos=709,
            inner=" symbol, you can write ",
            enclosing=EnclosingPattern(left="", right=""),
            at_prefix=False,
        ),
        Text(
            start_pos=713,
            end_pos=721,
            inner='@#""@""#',
            enclosing=EnclosingPattern(left='##"', right='"##'),
            at_prefix=True,
        ),
        Text(
            start_pos=724,
            end_pos=744,
            inner=".\nIn turn, to write ",
            enclosing=EnclosingPattern(left="", right=""),
            at_prefix=False,
        ),
        Text(
            start_pos=748,
            end_pos=756,
            inner='@#""@""#',
            enclosing=EnclosingPattern(left='##"', right='"##'),
            at_prefix=True,
        ),
        Text(
            start_pos=759,
            end_pos=788,
            inner=" as-is, you can do by typing ",
            enclosing=EnclosingPattern(left="", right=""),
            at_prefix=False,
        ),
        Text(
            start_pos=793,
            end_pos=808,
            inner='@##"@#""@""#"##',
            enclosing=EnclosingPattern(left='###"', right='"###'),
            at_prefix=True,
        ),
        Text(
            start_pos=812,
            end_pos=815,
            inner=".\n\n",
            enclosing=EnclosingPattern(left="", right=""),
            at_prefix=False,
        ),
        Command(
            start_pos=816,
            end_pos=882,
            intro="python",
            intro_enclosing=EnclosingPattern(left="", right=""),
            options=None,
            main_arg=Text(
                start_pos=825,
                end_pos=879,
                inner="\n    def is_odd(value):\n        return value % 2 == 1\n",
                enclosing=EnclosingPattern(left='##"', right='"##'),
                at_prefix=False,
            ),
        ),
        Text(
            start_pos=882,
            end_pos=898,
            inner="\\\nOdd digits are",
            enclosing=EnclosingPattern(left="", right=""),
            at_prefix=False,
        ),
        Command(
            start_pos=899,
            end_pos=955,
            intro="flatten",
            intro_enclosing=EnclosingPattern(left="", right=""),
            options=None,
            main_arg=FragmentList(
                start_pos=907,
                end_pos=954,
                children=[
                    Command(
                        start_pos=908,
                        end_pos=954,
                        intro="for",
                        intro_enclosing=EnclosingPattern(left="", right=""),
                        options=TokenList(
                            start_pos=912,
                            end_pos=929,
                            children=[
                                Identifier(start_pos=912, end_pos=913, name="i"),
                                Identifier(start_pos=914, end_pos=916, name="in"),
                                Command(
                                    start_pos=918,
                                    end_pos=929,
                                    intro="range(10)",
                                    intro_enclosing=EnclosingPattern(
                                        left="|", right="|"
                                    ),
                                    options=None,
                                    main_arg=None,
                                ),
                            ],
                        ),
                        main_arg=FragmentList(
                            start_pos=931,
                            end_pos=953,
                            children=[
                                Command(
                                    start_pos=932,
                                    end_pos=953,
                                    intro="if",
                                    intro_enclosing=EnclosingPattern(left="", right=""),
                                    options=TokenList(
                                        start_pos=935,
                                        end_pos=947,
                                        children=[
                                            Command(
                                                start_pos=936,
                                                end_pos=947,
                                                intro="is_odd(i)",
                                                intro_enclosing=EnclosingPattern(
                                                    left="|", right="|"
                                                ),
                                                options=None,
                                                main_arg=None,
                                            )
                                        ],
                                    ),
                                    main_arg=FragmentList(
                                        start_pos=949,
                                        end_pos=952,
                                        children=[
                                            Text(
                                                start_pos=949,
                                                end_pos=950,
                                                inner=" ",
                                                enclosing=EnclosingPattern(
                                                    left="", right=""
                                                ),
                                                at_prefix=False,
                                            ),
                                            Command(
                                                start_pos=951,
                                                end_pos=952,
                                                intro="i",
                                                intro_enclosing=EnclosingPattern(
                                                    left="", right=""
                                                ),
                                                options=None,
                                                main_arg=None,
                                            ),
                                        ],
                                        enclosing=EnclosingPattern(left="{", right="}"),
                                        at_prefix=False,
                                    ),
                                )
                            ],
                            enclosing=EnclosingPattern(left="{", right="}"),
                            at_prefix=False,
                        ),
                    )
                ],
                enclosing=EnclosingPattern(left="{", right="}"),
                at_prefix=False,
            ),
        ),
        Text(
            start_pos=955,
            end_pos=995,
            inner=".\nExpected outcome for rolling a die is ",
            enclosing=EnclosingPattern(left="", right=""),
            at_prefix=False,
        ),
        Command(
            start_pos=996,
            end_pos=1029,
            intro="statistics.mean",
            intro_enclosing=EnclosingPattern(left="|", right="|"),
            options=TokenList(
                start_pos=1014,
                end_pos=1028,
                children=[
                    Command(
                        start_pos=1015,
                        end_pos=1028,
                        intro="range(1, 7)",
                        intro_enclosing=EnclosingPattern(left="|", right="|"),
                        options=None,
                        main_arg=None,
                    )
                ],
            ),
            main_arg=None,
        ),
        Text(
            start_pos=1029,
            end_pos=1031,
            inner=".\n",
            enclosing=EnclosingPattern(left="", right=""),
            at_prefix=False,
        ),
    ],
    enclosing=GlobalEnclosingPattern(),
    at_prefix=False,
)
```

If we are using the Python authoring mode
(a renderer extension provided by Paxter library package)
to process the intermediate parsed tree result from above,
then the following output result would be returned.

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

Learn more about Paxter via the following links from
[ReadTheDocs documentation](https://paxter.readthedocs.io/) website:
 
-   [Installation and Getting Started](https://paxter.readthedocs.io/en/latest/getting_started.html)
-   [Paxter Language Tutorial](https://paxter.readthedocs.io/en/latest/paxter_language_tutorial.html)
-   [Python Authoring Mode Tutorial](https://paxter.readthedocs.io/en/latest/python_authoring_mode_tutorial.html)
-   [Custom Renderer Tutorial](https://paxter.readthedocs.io/en/latest/custom_renderer_tutorial.html)
-   [Syntax Reference](https://paxter.readthedocs.io/en/latest/syntax.html)
-   [Core API Reference](https://paxter.readthedocs.io/en/latest/core_api.html)
-   and more coming soon!


## Future Plans

-   Experiment with different kinds of transformers and use it in real life
-   Re-implementing lexers and parsers in Rust for better performance
    and portability to other environments (such as WASM). 
-   And more!


## Development

`Makefile` contains a lot of utility scripts.  
See help command by simply running `make` or `make help`.
