import pytest

from paxter.parser import (
    Command, EnclosingPattern, FragmentSeq, GlobalEnclosingPattern, Identifier,
    Number, Operator, ParseContext, Text, Token, TokenSeq,
)


@pytest.mark.parametrize(
    ("input_text", "expected"),
    [
        pytest.param(
            '',
            FragmentSeq(
                start_pos=0, end_pos=0,
                children=[],
                enclosing=GlobalEnclosingPattern(),
            ),
        ),
        pytest.param(
            '1',
            FragmentSeq(
                start_pos=0, end_pos=1,
                children=[
                    Text(
                        start_pos=0, end_pos=1,
                        inner="1",
                        enclosing=EnclosingPattern(left="", right=""),
                    ),
                ],
                enclosing=GlobalEnclosingPattern(),
            ),
        ),
        pytest.param(
            '@hello',
            FragmentSeq(
                start_pos=0, end_pos=6,
                children=[
                    Command(
                        start_pos=1, end_pos=6,
                        phrase="hello",
                        phrase_enclosing=EnclosingPattern(left="", right=""),
                        option=None,
                        main_arg=None,
                    ),
                ],
                enclosing=GlobalEnclosingPattern(),
            ),
        ),
        pytest.param(
            'Hello, my name is @name.',
            FragmentSeq(
                start_pos=0, end_pos=24,
                children=[
                    Text(
                        start_pos=0, end_pos=18,
                        inner="Hello, my name is ",
                        enclosing=EnclosingPattern(left="", right=""),
                    ),
                    Command(
                        start_pos=19, end_pos=23,
                        phrase="name",
                        phrase_enclosing=EnclosingPattern(left="", right=""),
                        option=None,
                        main_arg=None,
                    ),
                    Text(
                        start_pos=23, end_pos=24,
                        inner=".",
                        enclosing=EnclosingPattern(left="", right=""),
                    ),
                ],
                enclosing=GlobalEnclosingPattern(),
            ),
        ),
        pytest.param(
            'The result of 1 + 1 is @|1 + 1|. Yes! @##|1 + 1|##',
            FragmentSeq(
                start_pos=0, end_pos=50,
                children=[
                    Text(
                        start_pos=0, end_pos=23,
                        inner="The result of 1 + 1 is ",
                        enclosing=EnclosingPattern(left="", right=""),
                    ),
                    Command(
                        start_pos=24, end_pos=31,
                        phrase="1 + 1",
                        phrase_enclosing=EnclosingPattern(left="|", right="|"),
                        option=None,
                        main_arg=None,
                    ),
                    Text(
                        start_pos=31, end_pos=38,
                        inner=". Yes! ",
                        enclosing=EnclosingPattern(left="", right=""),
                    ),
                    Command(
                        start_pos=39, end_pos=50,
                        phrase="1 + 1",
                        phrase_enclosing=EnclosingPattern(left="##|", right="|##"),
                        option=None,
                        main_arg=None,
                    ),
                ],
                enclosing=GlobalEnclosingPattern(),
            ),
        ),
        pytest.param(
            '@|N @ M @ K|',
            FragmentSeq(
                start_pos=0, end_pos=12,
                children=[
                    Command(
                        start_pos=1, end_pos=12,
                        phrase="N @ M @ K",
                        phrase_enclosing=EnclosingPattern(left="|", right="|"),
                        option=None,
                        main_arg=None,
                    ),
                ],
                enclosing=GlobalEnclosingPattern(),
            ),
        ),
        pytest.param(
            '@##|#|#|#|## @||@|@|@|,|@|;|@|#|@#|||#  @@@,@;@#@@@"@{@}',
            FragmentSeq(
                start_pos=0, end_pos=56,
                children=[
                    Command(
                        start_pos=1, end_pos=12,
                        phrase="#|#|#",
                        phrase_enclosing=EnclosingPattern(left="##|", right="|##"),
                        option=None,
                        main_arg=None,
                    ),
                    Text(
                        start_pos=12, end_pos=13,
                        inner=" ",
                        enclosing=EnclosingPattern(left="", right=""),
                    ),
                    Command(
                        start_pos=14, end_pos=16,
                        phrase="",
                        phrase_enclosing=EnclosingPattern(left="|", right="|"),
                        option=None,
                        main_arg=None,
                    ),
                    Command(
                        start_pos=17, end_pos=20,
                        phrase="@",
                        phrase_enclosing=EnclosingPattern(left="|", right="|"),
                        option=None,
                        main_arg=None,
                    ),
                    Command(
                        start_pos=21, end_pos=24,
                        phrase=",",
                        phrase_enclosing=EnclosingPattern(left="|", right="|"),
                        option=None,
                        main_arg=None,
                    ),
                    Command(
                        start_pos=25, end_pos=28,
                        phrase=";",
                        phrase_enclosing=EnclosingPattern(left="|", right="|"),
                        option=None,
                        main_arg=None,
                    ),
                    Command(
                        start_pos=29, end_pos=32,
                        phrase="#",
                        phrase_enclosing=EnclosingPattern(left="|", right="|"),
                        option=None,
                        main_arg=None,
                    ),
                    Command(
                        start_pos=33, end_pos=38,
                        phrase="|",
                        phrase_enclosing=EnclosingPattern(left="#|", right="|#"),
                        option=None,
                        main_arg=None,
                    ),
                    Text(
                        start_pos=38, end_pos=40,
                        inner="  ",
                        enclosing=EnclosingPattern(left="", right=""),
                    ),
                    Command(
                        start_pos=41, end_pos=42,
                        phrase="@",
                        phrase_enclosing=EnclosingPattern(left="", right=""),
                        option=None,
                        main_arg=None,
                    ),
                    Command(
                        start_pos=43, end_pos=44,
                        phrase=",",
                        phrase_enclosing=EnclosingPattern(left="", right=""),
                        option=None,
                        main_arg=None,
                    ),
                    Command(
                        start_pos=45, end_pos=46,
                        phrase=";",
                        phrase_enclosing=EnclosingPattern(left="", right=""),
                        option=None,
                        main_arg=None,
                    ),
                    Command(
                        start_pos=47, end_pos=48,
                        phrase="#",
                        phrase_enclosing=EnclosingPattern(left="", right=""),
                        option=None,
                        main_arg=None,
                    ),
                    Command(
                        start_pos=49, end_pos=50,
                        phrase="@",
                        phrase_enclosing=EnclosingPattern(left="", right=""),
                        option=None,
                        main_arg=None,
                    ),
                    Command(
                        start_pos=51, end_pos=52,
                        phrase='"',
                        phrase_enclosing=EnclosingPattern(left="", right=""),
                        option=None,
                        main_arg=None,
                    ),
                    Command(
                        start_pos=53, end_pos=54,
                        phrase="{",
                        phrase_enclosing=EnclosingPattern(left="", right=""),
                        option=None,
                        main_arg=None,
                    ),
                    Command(
                        start_pos=55, end_pos=56,
                        phrase="}",
                        phrase_enclosing=EnclosingPattern(left="", right=""),
                        option=None,
                        main_arg=None,
                    ),
                ],
                enclosing=GlobalEnclosingPattern(),
            ),
        ),
        pytest.param(
            'This is @em{not} a drill!',
            FragmentSeq(
                start_pos=0, end_pos=25,
                children=[
                    Text(
                        start_pos=0, end_pos=8,
                        inner="This is ",
                        enclosing=EnclosingPattern(left="", right=""),
                    ),
                    Command(
                        start_pos=9, end_pos=16,
                        phrase="em",
                        phrase_enclosing=EnclosingPattern(left="", right=""),
                        option=None,
                        main_arg=FragmentSeq(
                            start_pos=12, end_pos=15,
                            children=[
                                Text(
                                    start_pos=12, end_pos=15,
                                    inner="not",
                                    enclosing=EnclosingPattern(left="", right=""),
                                ),
                            ],
                            enclosing=EnclosingPattern(left="{", right="}"),
                        ),
                    ),
                    Text(
                        start_pos=16, end_pos=25,
                        inner=" a drill!",
                        enclosing=EnclosingPattern(left="", right=""),
                    ),
                ],
                enclosing=GlobalEnclosingPattern(),
            ),
        ),
        pytest.param(
            '@|foo.process|{yes} @#|foo#process|#["no"]#"#"#',
            FragmentSeq(
                start_pos=0, end_pos=47,
                children=[
                    Command(
                        start_pos=1, end_pos=19,
                        phrase="foo.process",
                        phrase_enclosing=EnclosingPattern(left="|", right="|"),
                        option=None,
                        main_arg=FragmentSeq(
                            start_pos=15, end_pos=18,
                            children=[
                                Text(
                                    start_pos=15, end_pos=18,
                                    inner="yes",
                                    enclosing=EnclosingPattern(left="", right=""),
                                ),
                            ],
                            enclosing=EnclosingPattern(left="{", right="}"),
                        ),
                    ),
                    Text(
                        start_pos=19, end_pos=20,
                        inner=" ",
                        enclosing=EnclosingPattern(left="", right=""),
                    ),
                    Command(
                        start_pos=21, end_pos=47,
                        phrase="foo#process",
                        phrase_enclosing=EnclosingPattern(left="#|", right="|#"),
                        option=TokenSeq(
                            start_pos=37, end_pos=41,
                            children=[
                                Text(
                                    start_pos=38, end_pos=40,
                                    inner="no",
                                    enclosing=EnclosingPattern(left='"', right='"'),
                                ),
                            ],
                        ),
                        main_arg=Text(
                            start_pos=44, end_pos=45,
                            inner="#",
                            enclosing=EnclosingPattern(left='#"', right='"#'),
                        ),
                    ),
                ],
                enclosing=GlobalEnclosingPattern(),
            ),
        ),
        pytest.param(
            "Level 0 @level1{ @level2{ @level3 } }",
            FragmentSeq(
                start_pos=0, end_pos=37,
                children=[
                    Text(
                        start_pos=0, end_pos=8,
                        inner="Level 0 ",
                        enclosing=EnclosingPattern(left="", right=""),
                    ),
                    Command(
                        start_pos=9, end_pos=37,
                        phrase="level1",
                        phrase_enclosing=EnclosingPattern(left="", right=""),
                        option=None,
                        main_arg=FragmentSeq(
                            start_pos=16, end_pos=36,
                            children=[
                                Text(
                                    start_pos=16, end_pos=17,
                                    inner=" ",
                                    enclosing=EnclosingPattern(left="", right=""),
                                ),
                                Command(
                                    start_pos=18, end_pos=35,
                                    phrase="level2",
                                    phrase_enclosing=EnclosingPattern(
                                        left="", right="",
                                    ),
                                    option=None,
                                    main_arg=FragmentSeq(
                                        start_pos=25, end_pos=34,
                                        children=[
                                            Text(
                                                start_pos=25, end_pos=26,
                                                inner=" ",
                                                enclosing=EnclosingPattern(
                                                    left="", right="",
                                                ),
                                            ),
                                            Command(
                                                start_pos=27, end_pos=33,
                                                phrase="level3",
                                                phrase_enclosing=EnclosingPattern(
                                                    left="", right="",
                                                ),
                                                option=None,
                                                main_arg=None,
                                            ),
                                            Text(
                                                start_pos=33, end_pos=34,
                                                inner=" ",
                                                enclosing=EnclosingPattern(
                                                    left="", right="",
                                                ),
                                            ),
                                        ],
                                        enclosing=EnclosingPattern(left="{", right="}"),
                                    ),
                                ),
                                Text(
                                    start_pos=35, end_pos=36,
                                    inner=" ",
                                    enclosing=EnclosingPattern(left="", right=""),
                                ),
                            ],
                            enclosing=EnclosingPattern(left="{", right="}"),
                        ),
                    ),
                ],
                enclosing=GlobalEnclosingPattern(),
            ),
        ),
        pytest.param(
            '@say[greet=##"hello"##]{John} at @email##"john@example.com"##!',
            FragmentSeq(
                start_pos=0, end_pos=62,
                children=[
                    Command(
                        start_pos=1, end_pos=29,
                        phrase="say",
                        phrase_enclosing=EnclosingPattern(left="", right=""),
                        option=TokenSeq(
                            start_pos=5, end_pos=22,
                            children=[
                                Identifier(start_pos=5, end_pos=10, name="greet"),
                                Operator(start_pos=10, end_pos=11, symbols="="),
                                Text(
                                    start_pos=14, end_pos=19,
                                    inner="hello",
                                    enclosing=EnclosingPattern(left='##"', right='"##'),
                                ),
                            ],
                        ),
                        main_arg=FragmentSeq(
                            start_pos=24, end_pos=28,
                            children=[
                                Text(
                                    start_pos=24, end_pos=28,
                                    inner="John",
                                    enclosing=EnclosingPattern(left="", right=""),
                                ),
                            ],
                            enclosing=EnclosingPattern(left="{", right="}"),
                        ),
                    ),
                    Text(
                        start_pos=29, end_pos=33,
                        inner=" at ",
                        enclosing=EnclosingPattern(left="", right=""),
                    ),
                    Command(
                        start_pos=34, end_pos=61,
                        phrase="email",
                        phrase_enclosing=EnclosingPattern(left="", right=""),
                        option=None,
                        main_arg=Text(
                            start_pos=42, end_pos=58,
                            inner="john@example.com",
                            enclosing=EnclosingPattern(left='##"', right='"##'),
                        ),
                    ),
                    Text(
                        start_pos=61, end_pos=62,
                        inner="!",
                        enclosing=EnclosingPattern(left="", right=""),
                    ),
                ],
                enclosing=GlobalEnclosingPattern(),
            ),
        ),
        pytest.param(
            '@###|state|###[x=1] @state[x=2]',
            FragmentSeq(
                start_pos=0, end_pos=31,
                children=[
                    Command(
                        start_pos=1, end_pos=19,
                        phrase="state",
                        phrase_enclosing=EnclosingPattern(left="###|", right="|###"),
                        option=TokenSeq(
                            start_pos=15, end_pos=18,
                            children=[
                                Identifier(start_pos=15, end_pos=16, name="x"),
                                Operator(start_pos=16, end_pos=17, symbols="="),
                                Number(start_pos=17, end_pos=18, value=1),
                            ],
                        ),
                        main_arg=None,
                    ),
                    Text(
                        start_pos=19, end_pos=20,
                        inner=" ",
                        enclosing=EnclosingPattern(left="", right=""),
                    ),
                    Command(
                        start_pos=21, end_pos=31,
                        phrase="state",
                        phrase_enclosing=EnclosingPattern(left="", right=""),
                        option=TokenSeq(
                            start_pos=27, end_pos=30,
                            children=[
                                Identifier(start_pos=27, end_pos=28, name="x"),
                                Operator(start_pos=28, end_pos=29, symbols="="),
                                Number(start_pos=29, end_pos=30, value=2),
                            ],
                        ),
                        main_arg=None,
                    ),
                ],
                enclosing=GlobalEnclosingPattern(),
            ),
        ),
        pytest.param(
            '@state[x=1,y=2,z=3]#"This symbol " is a quote!"#',
            FragmentSeq(
                start_pos=0, end_pos=48,
                children=[
                    Command(
                        start_pos=1, end_pos=48,
                        phrase="state",
                        phrase_enclosing=EnclosingPattern(left="", right=""),
                        option=TokenSeq(
                            start_pos=7, end_pos=18,
                            children=[
                                Identifier(start_pos=7, end_pos=8, name="x"),
                                Operator(start_pos=8, end_pos=9, symbols="="),
                                Number(start_pos=9, end_pos=10, value=1),
                                Operator(start_pos=10, end_pos=11, symbols=","),
                                Identifier(start_pos=11, end_pos=12, name="y"),
                                Operator(start_pos=12, end_pos=13, symbols="="),
                                Number(start_pos=13, end_pos=14, value=2),
                                Operator(start_pos=14, end_pos=15, symbols=","),
                                Identifier(start_pos=15, end_pos=16, name="z"),
                                Operator(start_pos=16, end_pos=17, symbols="="),
                                Number(start_pos=17, end_pos=18, value=3),
                            ],
                        ),
                        main_arg=Text(
                            start_pos=21, end_pos=46,
                            inner='This symbol " is a quote!',
                            enclosing=EnclosingPattern(left='#"', right='"#'),
                        ),
                    ),
                ],
                enclosing=GlobalEnclosingPattern(),
            ),
        ),
        pytest.param(
            '@|| @#||# @foo[{@bar}"@baz"##{}###""#]',
            FragmentSeq(
                start_pos=0,
                end_pos=38,
                children=[
                    Command(
                        start_pos=1, end_pos=3,
                        phrase="",
                        phrase_enclosing=EnclosingPattern(left="|", right="|"),
                        option=None,
                        main_arg=None,
                    ),
                    Text(
                        start_pos=3, end_pos=4,
                        inner=" ",
                        enclosing=EnclosingPattern(left="", right=""),
                    ),
                    Command(
                        start_pos=5, end_pos=9,
                        phrase="",
                        phrase_enclosing=EnclosingPattern(left="#|", right="|#"),
                        option=None,
                        main_arg=None,
                    ),
                    Text(
                        start_pos=9, end_pos=10,
                        inner=" ",
                        enclosing=EnclosingPattern(left="", right=""),
                    ),
                    Command(
                        start_pos=11, end_pos=38,
                        phrase="foo",
                        phrase_enclosing=EnclosingPattern(left="", right=""),
                        option=TokenSeq(
                            start_pos=15, end_pos=37,
                            children=[
                                FragmentSeq(
                                    start_pos=16, end_pos=20,
                                    children=[
                                        Command(
                                            start_pos=17, end_pos=20,
                                            phrase="bar",
                                            phrase_enclosing=EnclosingPattern(
                                                left="", right="",
                                            ),
                                            option=None,
                                            main_arg=None,
                                        ),
                                    ],
                                    enclosing=EnclosingPattern(left="{", right="}"),
                                ),
                                Text(
                                    start_pos=22, end_pos=26,
                                    inner="@baz",
                                    enclosing=EnclosingPattern(left='"', right='"'),
                                ),
                                FragmentSeq(
                                    start_pos=30, end_pos=30,
                                    children=[],
                                    enclosing=EnclosingPattern(left="##{", right="}##"),
                                ),
                                Text(
                                    start_pos=35, end_pos=35,
                                    inner="",
                                    enclosing=EnclosingPattern(left='#"', right='"#'),
                                ),
                            ],
                        ),
                        main_arg=None,
                    ),
                ],
                enclosing=GlobalEnclosingPattern(),
            ),
        ),
        pytest.param(
            '@foo[bar = "x" + @|foo|[bar={x@x}|>3]]',
            FragmentSeq(
                start_pos=0, end_pos=38,
                children=[
                    Command(
                        start_pos=1, end_pos=38,
                        phrase="foo",
                        phrase_enclosing=EnclosingPattern(left="", right=""),
                        option=TokenSeq(
                            start_pos=5, end_pos=37,
                            children=[
                                Identifier(start_pos=5, end_pos=8, name="bar"),
                                Operator(start_pos=9, end_pos=10, symbols="="),
                                Text(
                                    start_pos=12, end_pos=13,
                                    inner="x",
                                    enclosing=EnclosingPattern(left='"', right='"'),
                                ),
                                Operator(start_pos=15, end_pos=16, symbols="+"),
                                Command(
                                    start_pos=18, end_pos=37,
                                    phrase="foo",
                                    phrase_enclosing=EnclosingPattern(
                                        left="|", right="|",
                                    ),
                                    option=TokenSeq(
                                        start_pos=24, end_pos=36,
                                        children=[
                                            Identifier(
                                                start_pos=24, end_pos=27,
                                                name="bar",
                                            ),
                                            Operator(
                                                start_pos=27, end_pos=28,
                                                symbols="=",
                                            ),
                                            FragmentSeq(
                                                start_pos=29,
                                                end_pos=32,
                                                children=[
                                                    Text(
                                                        start_pos=29, end_pos=30,
                                                        inner="x",
                                                        enclosing=EnclosingPattern(
                                                            left="", right="",
                                                        ),
                                                    ),
                                                    Command(
                                                        start_pos=31, end_pos=32,
                                                        phrase="x",
                                                        phrase_enclosing=(
                                                                EnclosingPattern(
                                                                    left="", right="",
                                                                )
                                                        ),
                                                        option=None,
                                                        main_arg=None,
                                                    ),
                                                ],
                                                enclosing=EnclosingPattern(
                                                    left="{", right="}",
                                                ),
                                            ),
                                            Operator(
                                                start_pos=33, end_pos=35,
                                                symbols="|>",
                                            ),
                                            Number(start_pos=35, end_pos=36, value=3),
                                        ],
                                    ),
                                    main_arg=None,
                                ),
                            ],
                        ),
                        main_arg=None,
                    ),
                ],
                enclosing=GlobalEnclosingPattern(),
            ),
        ),
        pytest.param(
            '@x{@expand[1->2,<-3,stop,"foo",{bar},,@|cool.fm|]{@|4+4|}}',
            FragmentSeq(
                start_pos=0, end_pos=58,
                children=[
                    Command(
                        start_pos=1, end_pos=58,
                        phrase="x",
                        phrase_enclosing=EnclosingPattern(left="", right=""),
                        option=None,
                        main_arg=FragmentSeq(
                            start_pos=3, end_pos=57,
                            children=[
                                Command(
                                    start_pos=4, end_pos=57,
                                    phrase="expand",
                                    phrase_enclosing=EnclosingPattern(
                                        left="", right="",
                                    ),
                                    option=TokenSeq(
                                        start_pos=11, end_pos=48,
                                        children=[
                                            Number(start_pos=11, end_pos=12, value=1),
                                            Operator(
                                                start_pos=12, end_pos=14,
                                                symbols="->",
                                            ),
                                            Number(start_pos=14, end_pos=15, value=2),
                                            Operator(
                                                start_pos=15, end_pos=16,
                                                symbols=",",
                                            ),
                                            Operator(
                                                start_pos=16, end_pos=18,
                                                symbols="<-",
                                            ),
                                            Number(start_pos=18, end_pos=19, value=3),
                                            Operator(
                                                start_pos=19, end_pos=20,
                                                symbols=",",
                                            ),
                                            Identifier(
                                                start_pos=20, end_pos=24,
                                                name="stop",
                                            ),
                                            Operator(
                                                start_pos=24, end_pos=25,
                                                symbols=",",
                                            ),
                                            Text(
                                                start_pos=26,
                                                end_pos=29,
                                                inner="foo",
                                                enclosing=EnclosingPattern(
                                                    left='"', right='"',
                                                ),
                                            ),
                                            Operator(
                                                start_pos=30, end_pos=31,
                                                symbols=",",
                                            ),
                                            FragmentSeq(
                                                start_pos=32, end_pos=35,
                                                children=[
                                                    Text(
                                                        start_pos=32, end_pos=35,
                                                        inner="bar",
                                                        enclosing=EnclosingPattern(
                                                            left="", right="",
                                                        ),
                                                    ),
                                                ],
                                                enclosing=EnclosingPattern(
                                                    left="{", right="}",
                                                ),
                                            ),
                                            Operator(
                                                start_pos=36, end_pos=37,
                                                symbols=",",
                                            ),
                                            Operator(
                                                start_pos=37, end_pos=38,
                                                symbols=",",
                                            ),
                                            Command(
                                                start_pos=39, end_pos=48,
                                                phrase="cool.fm",
                                                phrase_enclosing=EnclosingPattern(
                                                    left="|", right="|",
                                                ),
                                                option=None,
                                                main_arg=None,
                                            ),
                                        ],
                                    ),
                                    main_arg=FragmentSeq(
                                        start_pos=50, end_pos=56,
                                        children=[
                                            Command(
                                                start_pos=51, end_pos=56,
                                                phrase="4+4",
                                                phrase_enclosing=EnclosingPattern(
                                                    left="|", right="|",
                                                ),
                                                option=None,
                                                main_arg=None,
                                            ),
                                        ],
                                        enclosing=EnclosingPattern(left="{", right="}"),
                                    ),
                                ),
                            ],
                            enclosing=EnclosingPattern(left="{", right="}"),
                        ),
                    ),
                ],
                enclosing=GlobalEnclosingPattern(),
            ),
        ),
        pytest.param(
            '@foo[[]->[],{}->[],@||]',
            FragmentSeq(
                start_pos=0, end_pos=23,
                children=[
                    Command(
                        start_pos=1, end_pos=23,
                        phrase="foo",
                        phrase_enclosing=EnclosingPattern(left="", right=""),
                        option=TokenSeq(
                            start_pos=5, end_pos=22,
                            children=[
                                TokenSeq(start_pos=6, end_pos=6, children=[]),
                                Operator(start_pos=7, end_pos=9, symbols="->"),
                                TokenSeq(start_pos=10, end_pos=10, children=[]),
                                Operator(start_pos=11, end_pos=12, symbols=","),
                                FragmentSeq(
                                    start_pos=13, end_pos=13,
                                    children=[],
                                    enclosing=EnclosingPattern(left="{", right="}"),
                                ),
                                Operator(start_pos=14, end_pos=16, symbols="->"),
                                TokenSeq(start_pos=17, end_pos=17, children=[]),
                                Operator(start_pos=18, end_pos=19, symbols=","),
                                Command(
                                    start_pos=20, end_pos=22,
                                    phrase="",
                                    phrase_enclosing=EnclosingPattern(
                                        left="|", right="|",
                                    ),
                                    option=None,
                                    main_arg=None,
                                ),
                            ],
                        ),
                        main_arg=None,
                    ),
                ],
                enclosing=GlobalEnclosingPattern(),
            ),
        ),
        pytest.param(
            '@foo[\n  a = {1 -> 2},\n  b = {My name is @name},\n]{bar}\n',
            FragmentSeq(
                start_pos=0, end_pos=55,
                children=[
                    Command(
                        start_pos=1, end_pos=54,
                        phrase="foo",
                        phrase_enclosing=EnclosingPattern(left="", right=""),
                        option=TokenSeq(
                            start_pos=5, end_pos=48,
                            children=[
                                Identifier(start_pos=8, end_pos=9, name="a"),
                                Operator(start_pos=10, end_pos=11, symbols="="),
                                FragmentSeq(
                                    start_pos=13, end_pos=19,
                                    children=[
                                        Text(
                                            start_pos=13, end_pos=19,
                                            inner="1 -> 2",
                                            enclosing=EnclosingPattern(
                                                left="", right="",
                                            ),
                                        ),
                                    ],
                                    enclosing=EnclosingPattern(left="{", right="}"),
                                ),
                                Operator(start_pos=20, end_pos=21, symbols=","),
                                Identifier(start_pos=24, end_pos=25, name="b"),
                                Operator(start_pos=26, end_pos=27, symbols="="),
                                FragmentSeq(
                                    start_pos=29, end_pos=45,
                                    children=[
                                        Text(
                                            start_pos=29, end_pos=40,
                                            inner="My name is ",
                                            enclosing=EnclosingPattern(
                                                left="", right="",
                                            ),
                                        ),
                                        Command(
                                            start_pos=41, end_pos=45,
                                            phrase="name",
                                            phrase_enclosing=EnclosingPattern(
                                                left="", right="",
                                            ),
                                            option=None,
                                            main_arg=None,
                                        ),
                                    ],
                                    enclosing=EnclosingPattern(left="{", right="}"),
                                ),
                                Operator(start_pos=46, end_pos=47, symbols=","),
                            ],
                        ),
                        main_arg=FragmentSeq(
                            start_pos=50, end_pos=53,
                            children=[
                                Text(
                                    start_pos=50, end_pos=53,
                                    inner="bar",
                                    enclosing=EnclosingPattern(left="", right=""),
                                ),
                            ],
                            enclosing=EnclosingPattern(left="{", right="}"),
                        ),
                    ),
                    Text(
                        start_pos=54, end_pos=55,
                        inner="\n",
                        enclosing=EnclosingPattern(left="", right=""),
                    ),
                ],
                enclosing=GlobalEnclosingPattern(),
            ),
        ),
    ],
)
def test_parser(input_text: str, expected: Token):
    tree = ParseContext(input_text).tree
    assert tree == expected
    assert tree.start_pos == expected.start_pos
    assert tree.end_pos == expected.end_pos
