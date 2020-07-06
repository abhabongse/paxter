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

-   The Paxter library package defines the syntax for **Paxter language**
    and provides a toolchain for parsing input texts
    written in Paxter language into _an intermediate parsed tree_.
-   However, the semantics of Paxter language is left unspecified,
    meaning that users of the library have all the freedom to do
    whatever they like to render or transform the intermediate parsed tree
    into a final output they wish to achieve.  
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

@python##"
    def tag(text, name='span'):
        return f'<{name}>{flatten(text)}</{name}>'
"##\
This is a very @tag["b"]{important @tag["i"]{feature}}:
@@-expressions are allowed to be nested within the main argument
using fragment list syntax (section surrounded by a pair of curly braces).

To escape right curly braces literal characters with the fragment list main argument,
simply enclose the main argument with as many #...# as you like
(@tag##{such as {this}!}##).

@python##"
    def is_odd(value):
        return value % 2 == 1
"##\
Odd digits are@flatten{@for[i in @|range(10)|]{@if[@|is_odd(i)|]{ @i}}}.
Expected outcome for rolling a die is @|statistics.mean|[@|range(1, 7)|].
```

Using the parser in Paxter library package to process this document,
we obtain the following result.

<details>
<summary>Click Here To Expand</summary>

```python
FragmentList(
    start_pos=0,
    end_pos=1263,
    children=[
        Command(
            start_pos=1,
            end_pos=248,
            starter="python",
            starter_enclosing=EnclosingPattern(left="", right=""),
            option=None,
            main_arg=Text(
                start_pos=10,
                end_pos=245,
                inner="\n    import statistics\n    from datetime import datetime\n\n    _symbols_ = {\n        '@': '@',\n        '.': '&hairsp;',\n        ',': '&thinsp;',\n    }\n    name = \"Ashley\"\n    birth_year = 1987\n    age = datetime.now().year - birth_year\n",
                enclosing=EnclosingPattern(left='##"', right='"##'),
            ),
        ),
        Text(
            start_pos=248,
            end_pos=261,
            inner="\\\nMy name is ",
            enclosing=EnclosingPattern(left="", right=""),
        ),
        Command(
            start_pos=262,
            end_pos=266,
            starter="name",
            starter_enclosing=EnclosingPattern(left="", right=""),
            option=None,
            main_arg=None,
        ),
        Text(
            start_pos=266,
            end_pos=276,
            inner=" and I am ",
            enclosing=EnclosingPattern(left="", right=""),
        ),
        Command(
            start_pos=277,
            end_pos=280,
            starter="age",
            starter_enclosing=EnclosingPattern(left="", right=""),
            option=None,
            main_arg=None,
        ),
        Text(
            start_pos=280,
            end_pos=310,
            inner=" years old.\nMy email is ashley",
            enclosing=EnclosingPattern(left="", right=""),
        ),
        SymbolCommand(start_pos=311, end_pos=312, symbol="@"),
        Text(
            start_pos=312,
            end_pos=345,
            inner="example.com.\nMy shop opens Monday",
            enclosing=EnclosingPattern(left="", right=""),
        ),
        SymbolCommand(start_pos=346, end_pos=347, symbol=","),
        Text(
            start_pos=347,
            end_pos=348,
            inner="-",
            enclosing=EnclosingPattern(left="", right=""),
        ),
        SymbolCommand(start_pos=349, end_pos=350, symbol=","),
        Text(
            start_pos=350,
            end_pos=359,
            inner="Friday.\n\n",
            enclosing=EnclosingPattern(left="", right=""),
        ),
        Command(
            start_pos=360,
            end_pos=434,
            starter="python",
            starter_enclosing=EnclosingPattern(left="", right=""),
            option=None,
            main_arg=Text(
                start_pos=369,
                end_pos=431,
                inner="\n    from itertools import count\n    counter = count(start=1)\n",
                enclosing=EnclosingPattern(left='##"', right='"##'),
            ),
        ),
        Text(
            start_pos=434,
            end_pos=459,
            inner="\\\nCounting is as easy as ",
            enclosing=EnclosingPattern(left="", right=""),
        ),
        Command(
            start_pos=460,
            end_pos=475,
            starter="next(counter)",
            starter_enclosing=EnclosingPattern(left="|", right="|"),
            option=None,
            main_arg=None,
        ),
        Text(
            start_pos=475,
            end_pos=477,
            inner=", ",
            enclosing=EnclosingPattern(left="", right=""),
        ),
        Command(
            start_pos=478,
            end_pos=493,
            starter="next(counter)",
            starter_enclosing=EnclosingPattern(left="|", right="|"),
            option=None,
            main_arg=None,
        ),
        Text(
            start_pos=493,
            end_pos=495,
            inner=", ",
            enclosing=EnclosingPattern(left="", right=""),
        ),
        Command(
            start_pos=496,
            end_pos=511,
            starter="next(counter)",
            starter_enclosing=EnclosingPattern(left="|", right="|"),
            option=None,
            main_arg=None,
        ),
        Text(
            start_pos=511,
            end_pos=554,
            inner=".\nArithmetic? Not a problem: 7 * 11 * 13 = ",
            enclosing=EnclosingPattern(left="", right=""),
        ),
        Command(
            start_pos=555,
            end_pos=568,
            starter="7 * 11 * 13",
            starter_enclosing=EnclosingPattern(left="|", right="|"),
            option=None,
            main_arg=None,
        ),
        Text(
            start_pos=568,
            end_pos=571,
            inner=".\n\n",
            enclosing=EnclosingPattern(left="", right=""),
        ),
        Command(
            start_pos=572,
            end_pos=668,
            starter="python",
            starter_enclosing=EnclosingPattern(left="", right=""),
            option=None,
            main_arg=Text(
                start_pos=581,
                end_pos=665,
                inner="\n    def tag(text, name='span'):\n        return f'<{name}>{flatten(text)}</{name}>'\n",
                enclosing=EnclosingPattern(left='##"', right='"##'),
            ),
        ),
        Text(
            start_pos=668,
            end_pos=685,
            inner="\\\nThis is a very ",
            enclosing=EnclosingPattern(left="", right=""),
        ),
        Command(
            start_pos=686,
            end_pos=724,
            starter="tag",
            starter_enclosing=EnclosingPattern(left="", right=""),
            option=TokenList(
                start_pos=690,
                end_pos=693,
                children=[
                    Text(
                        start_pos=691,
                        end_pos=692,
                        inner="b",
                        enclosing=EnclosingPattern(left='"', right='"'),
                    )
                ],
            ),
            main_arg=FragmentList(
                start_pos=695,
                end_pos=723,
                children=[
                    Text(
                        start_pos=695,
                        end_pos=705,
                        inner="important ",
                        enclosing=EnclosingPattern(left="", right=""),
                    ),
                    Command(
                        start_pos=706,
                        end_pos=723,
                        starter="tag",
                        starter_enclosing=EnclosingPattern(left="", right=""),
                        option=TokenList(
                            start_pos=710,
                            end_pos=713,
                            children=[
                                Text(
                                    start_pos=711,
                                    end_pos=712,
                                    inner="i",
                                    enclosing=EnclosingPattern(left='"', right='"'),
                                )
                            ],
                        ),
                        main_arg=FragmentList(
                            start_pos=715,
                            end_pos=722,
                            children=[
                                Text(
                                    start_pos=715,
                                    end_pos=722,
                                    inner="feature",
                                    enclosing=EnclosingPattern(left="", right=""),
                                )
                            ],
                            enclosing=EnclosingPattern(left="{", right="}"),
                        ),
                    ),
                ],
                enclosing=EnclosingPattern(left="{", right="}"),
            ),
        ),
        Text(
            start_pos=724,
            end_pos=726,
            inner=":\n",
            enclosing=EnclosingPattern(left="", right=""),
        ),
        SymbolCommand(start_pos=727, end_pos=728, symbol="@"),
        Text(
            start_pos=728,
            end_pos=1018,
            inner="-expressions are allowed to be nested within the main argument\nusing fragment list syntax (section surrounded by a pair of curly braces).\n\nTo escape right curly braces literal characters with the fragment list main argument,\nsimply enclose the main argument with as many #...# as you like\n(",
            enclosing=EnclosingPattern(left="", right=""),
        ),
        Command(
            start_pos=1019,
            end_pos=1043,
            starter="tag",
            starter_enclosing=EnclosingPattern(left="", right=""),
            option=None,
            main_arg=FragmentList(
                start_pos=1025,
                end_pos=1040,
                children=[
                    Text(
                        start_pos=1025,
                        end_pos=1040,
                        inner="such as {this}!",
                        enclosing=EnclosingPattern(left="", right=""),
                    )
                ],
                enclosing=EnclosingPattern(left="##{", right="}##"),
            ),
        ),
        Text(
            start_pos=1043,
            end_pos=1047,
            inner=").\n\n",
            enclosing=EnclosingPattern(left="", right=""),
        ),
        Command(
            start_pos=1048,
            end_pos=1114,
            starter="python",
            starter_enclosing=EnclosingPattern(left="", right=""),
            option=None,
            main_arg=Text(
                start_pos=1057,
                end_pos=1111,
                inner="\n    def is_odd(value):\n        return value % 2 == 1\n",
                enclosing=EnclosingPattern(left='##"', right='"##'),
            ),
        ),
        Text(
            start_pos=1114,
            end_pos=1130,
            inner="\\\nOdd digits are",
            enclosing=EnclosingPattern(left="", right=""),
        ),
        Command(
            start_pos=1131,
            end_pos=1187,
            starter="flatten",
            starter_enclosing=EnclosingPattern(left="", right=""),
            option=None,
            main_arg=FragmentList(
                start_pos=1139,
                end_pos=1186,
                children=[
                    Command(
                        start_pos=1140,
                        end_pos=1186,
                        starter="for",
                        starter_enclosing=EnclosingPattern(left="", right=""),
                        option=TokenList(
                            start_pos=1144,
                            end_pos=1161,
                            children=[
                                Identifier(start_pos=1144, end_pos=1145, name="i"),
                                Identifier(start_pos=1146, end_pos=1148, name="in"),
                                Command(
                                    start_pos=1150,
                                    end_pos=1161,
                                    starter="range(10)",
                                    starter_enclosing=EnclosingPattern(
                                        left="|", right="|"
                                    ),
                                    option=None,
                                    main_arg=None,
                                ),
                            ],
                        ),
                        main_arg=FragmentList(
                            start_pos=1163,
                            end_pos=1185,
                            children=[
                                Command(
                                    start_pos=1164,
                                    end_pos=1185,
                                    starter="if",
                                    starter_enclosing=EnclosingPattern(left="", right=""),
                                    option=TokenList(
                                        start_pos=1167,
                                        end_pos=1179,
                                        children=[
                                            Command(
                                                start_pos=1168,
                                                end_pos=1179,
                                                starter="is_odd(i)",
                                                starter_enclosing=EnclosingPattern(
                                                    left="|", right="|"
                                                ),
                                                option=None,
                                                main_arg=None,
                                            )
                                        ],
                                    ),
                                    main_arg=FragmentList(
                                        start_pos=1181,
                                        end_pos=1184,
                                        children=[
                                            Text(
                                                start_pos=1181,
                                                end_pos=1182,
                                                inner=" ",
                                                enclosing=EnclosingPattern(
                                                    left="", right=""
                                                ),
                                            ),
                                            Command(
                                                start_pos=1183,
                                                end_pos=1184,
                                                starter="i",
                                                starter_enclosing=EnclosingPattern(
                                                    left="", right=""
                                                ),
                                                option=None,
                                                main_arg=None,
                                            ),
                                        ],
                                        enclosing=EnclosingPattern(left="{", right="}"),
                                    ),
                                )
                            ],
                            enclosing=EnclosingPattern(left="{", right="}"),
                        ),
                    )
                ],
                enclosing=EnclosingPattern(left="{", right="}"),
            ),
        ),
        Text(
            start_pos=1187,
            end_pos=1227,
            inner=".\nExpected outcome for rolling a die is ",
            enclosing=EnclosingPattern(left="", right=""),
        ),
        Command(
            start_pos=1228,
            end_pos=1261,
            starter="statistics.mean",
            starter_enclosing=EnclosingPattern(left="|", right="|"),
            option=TokenList(
                start_pos=1246,
                end_pos=1260,
                children=[
                    Command(
                        start_pos=1247,
                        end_pos=1260,
                        starter="range(1, 7)",
                        starter_enclosing=EnclosingPattern(left="|", right="|"),
                        option=None,
                        main_arg=None,
                    )
                ],
            ),
            main_arg=None,
        ),
        Text(
            start_pos=1261,
            end_pos=1263,
            inner=".\n",
            enclosing=EnclosingPattern(left="", right=""),
        ),
    ],
    enclosing=GlobalEnclosingPattern(),
)
```
</details>

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

This is a very <b>important <i>feature</i></b>:
@-expressions are allowed to be nested within the main argument
using fragment list syntax (section surrounded by a pair of curly braces).

To escape right curly braces literal characters with the fragment list main argument,
simply enclose the main argument with as many #...# as you like
(<span>such as {this}!</span>).

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
