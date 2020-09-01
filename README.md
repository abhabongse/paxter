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
                    <a href="https://travis-ci.com/abhabongse/paxter"><img src="https://api.travis-ci.com/abhabongse/paxter.svg?branch=main" alt="Travis-CI Build Status" /></a>
                    <a href="https://requires.io/github/abhabongse/paxter/requirements/?branch=main"><img src="https://requires.io/github/abhabongse/paxter/requirements.svg?branch=main" alt="Requirements Status" /></a>
                    <a href="https://codecov.io/github/abhabongse/paxter"><img src="https://codecov.io/github/abhabongse/paxter/coverage.svg?branch=main" alt="Coverage Status" /></a>
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

**Paxter language** helps users write rich-formatting documents
with simple and easy-to-understand syntax.
Nevertheless, users still have access to the python environment:
they can call python functions and evaluate python expressions
right inside the document itself,
giving users flexibility and power to customize 
their approach to writing documents.

**Paxter package** is a document-first, text processing language toolchain,
inspired by [@-expressions in Racket](https://docs.racket-lang.org/scribble/reader.html).
Users of the package also has the access to the Paxter language parser API
which allows them to implement new interpreters on top of the Paxter language
if they so wish.


## Example

Suppose that we have written a document using Paxter language as shown below.

```text
@python##"
    import statistics
    from datetime import datetime
    from paxter.authoring.document import RawElement

    _extras_ = {
        '@': '@',
        ':': RawElement('&ensp;'),
    }
    name = "Ashley"
    birth_year = 1987
    age = datetime.now().year - birth_year
"##\
My name is @name and I am @age years old.
My email is ashley@@example.com.
My shop opens Monday@:-@:Friday.

@python##"
    from itertools import count
    counter = count(start=1)
"##\
Counting is as easy as @|next(counter)|, @|next(counter)|, @|next(counter)|.
Arithmetic? Not a problem: 7 * 11 * 13 = @|7 * 11 * 13|.

This is a very @bold{important @italic{feature}}:
@@-expressions are allowed to be nested within the main argument
using fragment list syntax (section surrounded by a pair of curly braces).

To escape right curly braces literal characters with the fragment list main argument,
simply enclose the main argument with as many #...# as you like
(@bold##{such as {this}!}##).

@python##"
    def is_odd(value):
        return value % 2 == 1
"##\
Odd digits are@for[i in @range[10]]{@if[@is_odd[@i]]{ @i}}.
Expected outcome for rolling a die is @|statistics.mean|[@|range(1, 7)|].
```

Using the parser from the Paxter library package to process the above input,
we obtain the following parsed tree.

<details>
<summary>Click Here To Expand</summary>

```python
FragmentSeq(
    start_pos=0,
    end_pos=1131,
    children=[
        Command(
            start_pos=1,
            end_pos=233,
            phrase="python",
            phrase_enclosing=EnclosingPattern(left="", right=""),
            options=None,
            main_arg=Text(
                start_pos=10,
                end_pos=230,
                inner="\n    import statistics\n    from datetime import datetime\n\n    _extras_ = {\n        '@': '@',\n        '.': '\u200a',\n        ',': '\u2009',\n    }\n    name = \"Ashley\"\n    birth_year = 1987\n    age = datetime.now().year - birth_year\n",
                enclosing=EnclosingPattern(left='##"', right='"##'),
            ),
        ),
        Text(
            start_pos=233,
            end_pos=246,
            inner="\\\nMy name is ",
            enclosing=EnclosingPattern(left="", right=""),
        ),
        Command(
            start_pos=247,
            end_pos=251,
            phrase="name",
            phrase_enclosing=EnclosingPattern(left="", right=""),
            options=None,
            main_arg=None,
        ),
        Text(
            start_pos=251,
            end_pos=261,
            inner=" and I am ",
            enclosing=EnclosingPattern(left="", right=""),
        ),
        Command(
            start_pos=262,
            end_pos=265,
            phrase="age",
            phrase_enclosing=EnclosingPattern(left="", right=""),
            options=None,
            main_arg=None,
        ),
        Text(
            start_pos=265,
            end_pos=295,
            inner=" years old.\nMy email is ashley",
            enclosing=EnclosingPattern(left="", right=""),
        ),
        Command(
            start_pos=296,
            end_pos=297,
            phrase="@",
            phrase_enclosing=EnclosingPattern(left="", right=""),
            options=None,
            main_arg=None,
        ),
        Text(
            start_pos=297,
            end_pos=330,
            inner="example.com.\nMy shop opens Monday",
            enclosing=EnclosingPattern(left="", right=""),
        ),
        Command(
            start_pos=331,
            end_pos=332,
            phrase=",",
            phrase_enclosing=EnclosingPattern(left="", right=""),
            options=None,
            main_arg=None,
        ),
        Text(
            start_pos=332,
            end_pos=333,
            inner="-",
            enclosing=EnclosingPattern(left="", right=""),
        ),
        Command(
            start_pos=334,
            end_pos=335,
            phrase=",",
            phrase_enclosing=EnclosingPattern(left="", right=""),
            options=None,
            main_arg=None,
        ),
        Text(
            start_pos=335,
            end_pos=344,
            inner="Friday.\n\n",
            enclosing=EnclosingPattern(left="", right=""),
        ),
        Command(
            start_pos=345,
            end_pos=419,
            phrase="python",
            phrase_enclosing=EnclosingPattern(left="", right=""),
            options=None,
            main_arg=Text(
                start_pos=354,
                end_pos=416,
                inner="\n    from itertools import count\n    counter = count(start=1)\n",
                enclosing=EnclosingPattern(left='##"', right='"##'),
            ),
        ),
        Text(
            start_pos=419,
            end_pos=444,
            inner="\\\nCounting is as easy as ",
            enclosing=EnclosingPattern(left="", right=""),
        ),
        Command(
            start_pos=445,
            end_pos=460,
            phrase="next(counter)",
            phrase_enclosing=EnclosingPattern(left="|", right="|"),
            options=None,
            main_arg=None,
        ),
        Text(
            start_pos=460,
            end_pos=462,
            inner=", ",
            enclosing=EnclosingPattern(left="", right=""),
        ),
        Command(
            start_pos=463,
            end_pos=478,
            phrase="next(counter)",
            phrase_enclosing=EnclosingPattern(left="|", right="|"),
            options=None,
            main_arg=None,
        ),
        Text(
            start_pos=478,
            end_pos=480,
            inner=", ",
            enclosing=EnclosingPattern(left="", right=""),
        ),
        Command(
            start_pos=481,
            end_pos=496,
            phrase="next(counter)",
            phrase_enclosing=EnclosingPattern(left="|", right="|"),
            options=None,
            main_arg=None,
        ),
        Text(
            start_pos=496,
            end_pos=539,
            inner=".\nArithmetic? Not a problem: 7 * 11 * 13 = ",
            enclosing=EnclosingPattern(left="", right=""),
        ),
        Command(
            start_pos=540,
            end_pos=553,
            phrase="7 * 11 * 13",
            phrase_enclosing=EnclosingPattern(left="|", right="|"),
            options=None,
            main_arg=None,
        ),
        Text(
            start_pos=553,
            end_pos=571,
            inner=".\n\nThis is a very ",
            enclosing=EnclosingPattern(left="", right=""),
        ),
        Command(
            start_pos=572,
            end_pos=604,
            phrase="bold",
            phrase_enclosing=EnclosingPattern(left="", right=""),
            options=None,
            main_arg=FragmentSeq(
                start_pos=577,
                end_pos=603,
                children=[
                    Text(
                        start_pos=577,
                        end_pos=587,
                        inner="important ",
                        enclosing=EnclosingPattern(left="", right=""),
                    ),
                    Command(
                        start_pos=588,
                        end_pos=603,
                        phrase="italic",
                        phrase_enclosing=EnclosingPattern(left="", right=""),
                        options=None,
                        main_arg=FragmentSeq(
                            start_pos=595,
                            end_pos=602,
                            children=[
                                Text(
                                    start_pos=595,
                                    end_pos=602,
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
            start_pos=604,
            end_pos=606,
            inner=":\n",
            enclosing=EnclosingPattern(left="", right=""),
        ),
        Command(
            start_pos=607,
            end_pos=608,
            phrase="@",
            phrase_enclosing=EnclosingPattern(left="", right=""),
            options=None,
            main_arg=None,
        ),
        Text(
            start_pos=608,
            end_pos=898,
            inner="-expressions are allowed to be nested within the main argument\nusing fragment list syntax (section surrounded by a pair of curly braces).\n\nTo escape right curly braces literal characters with the fragment list main argument,\nsimply enclose the main argument with as many #...# as you like\n(",
            enclosing=EnclosingPattern(left="", right=""),
        ),
        Command(
            start_pos=899,
            end_pos=924,
            phrase="bold",
            phrase_enclosing=EnclosingPattern(left="", right=""),
            options=None,
            main_arg=FragmentSeq(
                start_pos=906,
                end_pos=921,
                children=[
                    Text(
                        start_pos=906,
                        end_pos=921,
                        inner="such as {this}!",
                        enclosing=EnclosingPattern(left="", right=""),
                    )
                ],
                enclosing=EnclosingPattern(left="##{", right="}##"),
            ),
        ),
        Text(
            start_pos=924,
            end_pos=928,
            inner=").\n\n",
            enclosing=EnclosingPattern(left="", right=""),
        ),
        Command(
            start_pos=929,
            end_pos=995,
            phrase="python",
            phrase_enclosing=EnclosingPattern(left="", right=""),
            options=None,
            main_arg=Text(
                start_pos=938,
                end_pos=992,
                inner="\n    def is_odd(value):\n        return value % 2 == 1\n",
                enclosing=EnclosingPattern(left='##"', right='"##'),
            ),
        ),
        Text(
            start_pos=995,
            end_pos=1011,
            inner="\\\nOdd digits are",
            enclosing=EnclosingPattern(left="", right=""),
        ),
        Command(
            start_pos=1012,
            end_pos=1055,
            phrase="for",
            phrase_enclosing=EnclosingPattern(left="", right=""),
            options=TokenSeq(
                start_pos=1016,
                end_pos=1031,
                children=[
                    Identifier(start_pos=1016, end_pos=1017, name="i"),
                    Identifier(start_pos=1018, end_pos=1020, name="in"),
                    Command(
                        start_pos=1022,
                        end_pos=1031,
                        phrase="range",
                        phrase_enclosing=EnclosingPattern(left="", right=""),
                        options=TokenSeq(
                            start_pos=1028,
                            end_pos=1030,
                            children=[Number(start_pos=1028, end_pos=1030, value=10)],
                        ),
                        main_arg=None,
                    ),
                ],
            ),
            main_arg=FragmentSeq(
                start_pos=1033,
                end_pos=1054,
                children=[
                    Command(
                        start_pos=1034,
                        end_pos=1054,
                        phrase="if",
                        phrase_enclosing=EnclosingPattern(left="", right=""),
                        options=TokenSeq(
                            start_pos=1037,
                            end_pos=1048,
                            children=[
                                Command(
                                    start_pos=1038,
                                    end_pos=1048,
                                    phrase="is_odd",
                                    phrase_enclosing=EnclosingPattern(
                                        left="", right=""
                                    ),
                                    options=TokenSeq(
                                        start_pos=1045,
                                        end_pos=1047,
                                        children=[
                                            Command(
                                                start_pos=1046,
                                                end_pos=1047,
                                                phrase="i",
                                                phrase_enclosing=EnclosingPattern(
                                                    left="", right=""
                                                ),
                                                options=None,
                                                main_arg=None,
                                            )
                                        ],
                                    ),
                                    main_arg=None,
                                )
                            ],
                        ),
                        main_arg=FragmentSeq(
                            start_pos=1050,
                            end_pos=1053,
                            children=[
                                Text(
                                    start_pos=1050,
                                    end_pos=1051,
                                    inner=" ",
                                    enclosing=EnclosingPattern(left="", right=""),
                                ),
                                Command(
                                    start_pos=1052,
                                    end_pos=1053,
                                    phrase="i",
                                    phrase_enclosing=EnclosingPattern(
                                        left="", right=""
                                    ),
                                    options=None,
                                    main_arg=None,
                                ),
                            ],
                            enclosing=EnclosingPattern(left="{", right="}"),
                        ),
                    )
                ],
                enclosing=EnclosingPattern(left="{", right="}"),
            ),
        ),
        Text(
            start_pos=1055,
            end_pos=1095,
            inner=".\nExpected outcome for rolling a die is ",
            enclosing=EnclosingPattern(left="", right=""),
        ),
        Command(
            start_pos=1096,
            end_pos=1129,
            phrase="statistics.mean",
            phrase_enclosing=EnclosingPattern(left="|", right="|"),
            options=TokenSeq(
                start_pos=1114,
                end_pos=1128,
                children=[
                    Command(
                        start_pos=1115,
                        end_pos=1128,
                        phrase="range(1, 7)",
                        phrase_enclosing=EnclosingPattern(left="|", right="|"),
                        options=None,
                        main_arg=None,
                    )
                ],
            ),
            main_arg=None,
        ),
        Text(
            start_pos=1129,
            end_pos=1131,
            inner=".\n",
            enclosing=EnclosingPattern(left="", right=""),
        ),
    ],
    enclosing=GlobalEnclosingPattern(),
)
```
</details>

But once we apply the evaluation to transformed the above parsed tree
into the the final document object using the supplementary
`paxter.authoring` submodule, we get the following result.

<details>
<summary>Click Here To Expand</summary>

```python
Document(
    blob=Fragments([
        Paragraph(
            blob=Fragments([
                "My name is Ashley and I am ",
                33,
                " years old.\nMy email is ashley@example.com.\nMy shop opens Monday",
                RawElement(blob="&ensp;"),
                "-",
                RawElement(blob="&ensp;"),
                "Friday.",
            ])
        ),
        Paragraph(
            blob=Fragments([
                "Counting is as easy as ",
                1,
                ", ",
                2,
                ", ",
                3,
                ".\nArithmetic? Not a problem: 7 * 11 * 13 = ",
                1001,
                ".",
            ])
        ),
        Paragraph(
            blob=Fragments([
                "This is a very ",
                Bold(blob=Fragments(["important ", Italic(blob=Fragments(["feature"]))])),
                ":\n@-expressions are allowed to be nested within the main argument\nusing fragment list syntax (section surrounded by a pair of curly braces).",
            ])
        ),
        Paragraph(
            blob=Fragments([
                "To escape right curly braces literal characters with the fragment list main argument,\nsimply enclose the main argument with as many #...# as you like\n(",
                Bold(blob=Fragments(["such as {this}!"])),
                ").",
            ]),
        ),
        Paragraph(
            blob=Fragments([
                "Odd digits are ",
                1,
                " ",
                3,
                " ",
                5,
                " ",
                7,
                " ",
                9,
                ".\nExpected outcome for rolling a die is ",
                3.5,
                ".",
            ]),
        ),
    ]),
)
```
</details>

Once we render the above `Document` instance into the final HTML output,
we will get the final output as shown below.

```html
<p>My name is Ashley and I am 33 years old.
   My email is ashley@example.com.
   My shop opens Monday&ensp;-&ensp;Friday.
</p>
<p>Counting is as easy as 1, 2, 3.
   Arithmetic? Not a problem: 7 * 11 * 13 = 1001.
</p>
<p>This is a very <b>important <i>feature</i></b>:
   @-expressions are allowed to be nested within the main argument
   using fragment list syntax (section surrounded by a pair of curly braces).
</p>
<p>To escape right curly braces literal characters with the fragment list main argument,
   simply enclose the main argument with as many #...# as you like
   (<b>such as {this}!</b>).
</p>
<p>Odd digits are 1 3 5 7 9.
   Expected outcome for rolling a die is 3.5.
</p>
```


## Documentation

Learn more about Paxter via the following links from
[ReadTheDocs documentation](https://paxter.readthedocs.io/) website.

## Future Plans

-   Experiment with different kinds of transformers and use it in real life
-   Re-implementing lexers and parsers in Rust for better performance
    and portability to other environments (such as WASM). 
-   And more!


## Development

`Makefile` contains a lot of utility scripts.  
See help command by simply running `make` or `make help`.
