import pytest

from paxter.core import (
    Command, EnclosingPattern, FragmentList, GlobalEnclosingPattern, Identifier,
    Number, Operator, ParseContext, Text, Token, TokenList,
)


@pytest.mark.parametrize(
    ("input_text", "expected"),
    [
        pytest.param(
            "",
            FragmentList(
                start_pos=0, end_pos=0,
                children=[],
                enclosing=GlobalEnclosingPattern(),
                at_prefix=False,
            ),
        ),
        pytest.param(
            "1",
            FragmentList(
                start_pos=0, end_pos=1,
                children=[
                    Text(
                        start_pos=0, end_pos=1,
                        inner="1",
                        enclosing=EnclosingPattern(left="", right=""),
                        at_prefix=False,
                    ),
                ],
                enclosing=GlobalEnclosingPattern(),
                at_prefix=False,
            ),
        ),
        pytest.param(
            "@hello",
            FragmentList(
                start_pos=0, end_pos=6,
                children=[
                    Command(
                        start_pos=1, end_pos=6,
                        intro="hello",
                        intro_enclosing=EnclosingPattern(left="", right=""),
                        options=None,
                        main_arg=None,
                    ),
                ],
                enclosing=GlobalEnclosingPattern(),
                at_prefix=False,
            ),
        ),
        pytest.param(
            "Hello, my name is @name.",
            FragmentList(
                start_pos=0, end_pos=24,
                children=[
                    Text(
                        start_pos=0, end_pos=18,
                        inner="Hello, my name is ",
                        enclosing=EnclosingPattern(left="", right=""),
                        at_prefix=False,
                    ),
                    Command(
                        start_pos=19, end_pos=23,
                        intro="name",
                        intro_enclosing=EnclosingPattern(left="", right=""),
                        options=None,
                        main_arg=None,
                    ),
                    Text(
                        start_pos=23, end_pos=24,
                        inner=".",
                        enclosing=EnclosingPattern(left="", right=""),
                        at_prefix=False,
                    ),
                ],
                enclosing=GlobalEnclosingPattern(),
                at_prefix=False,
            ),
        ),
        pytest.param(
            "The result of 1 + 1 is @|1 + 1|. Yes! @##|1 + 1|##",
            FragmentList(
                start_pos=0, end_pos=50,
                children=[
                    Text(
                        start_pos=0, end_pos=23,
                        inner="The result of 1 + 1 is ",
                        enclosing=EnclosingPattern(left="", right=""),
                        at_prefix=False,
                    ),
                    Command(
                        start_pos=24, end_pos=31,
                        intro="1 + 1",
                        intro_enclosing=EnclosingPattern(left="|", right="|"),
                        options=None,
                        main_arg=None,
                    ),
                    Text(
                        start_pos=31, end_pos=38,
                        inner=". Yes! ",
                        enclosing=EnclosingPattern(left="", right=""),
                        at_prefix=False,
                    ),
                    Command(
                        start_pos=39, end_pos=50,
                        intro="1 + 1",
                        intro_enclosing=EnclosingPattern(left="##|", right="|##"),
                        options=None,
                        main_arg=None,
                    ),
                ],
                enclosing=GlobalEnclosingPattern(),
                at_prefix=False,
            ),
        ),
        pytest.param(
            "@|N @ M @ K|",
            FragmentList(
                start_pos=0, end_pos=12,
                children=[
                    Command(
                        start_pos=1, end_pos=12,
                        intro="N @ M @ K",
                        intro_enclosing=EnclosingPattern(left="|", right="|"),
                        options=None,
                        main_arg=None,
                    ),
                ],
                enclosing=GlobalEnclosingPattern(),
                at_prefix=False,
            ),
        ),
        pytest.param(
            "@##|#|#|#|##, @@@,@;@#@@",
            FragmentList(
                start_pos=0, end_pos=24,
                children=[
                    Command(
                        start_pos=1, end_pos=12,
                        intro="#|#|#",
                        intro_enclosing=EnclosingPattern(left="##|", right="|##"),
                        options=None,
                        main_arg=None,
                    ),
                    Text(
                        start_pos=12, end_pos=14,
                        inner=", ",
                        enclosing=EnclosingPattern(left="", right=""),
                        at_prefix=False,
                    ),
                    Command(
                        start_pos=15, end_pos=16,
                        intro="@",
                        intro_enclosing=EnclosingPattern(left="", right=""),
                        options=None,
                        main_arg=None,
                    ),
                    Command(
                        start_pos=17, end_pos=18,
                        intro=",",
                        intro_enclosing=EnclosingPattern(left="", right=""),
                        options=None,
                        main_arg=None,
                    ),
                    Command(
                        start_pos=19, end_pos=20,
                        intro=";",
                        intro_enclosing=EnclosingPattern(left="", right=""),
                        options=None,
                        main_arg=None,
                    ),
                    Command(
                        start_pos=21, end_pos=22,
                        intro="#",
                        intro_enclosing=EnclosingPattern(left="", right=""),
                        options=None,
                        main_arg=None,
                    ),
                    Command(
                        start_pos=23, end_pos=24,
                        intro="@",
                        intro_enclosing=EnclosingPattern(left="", right=""),
                        options=None,
                        main_arg=None,
                    ),
                ],
                enclosing=GlobalEnclosingPattern(),
                at_prefix=False,
            ),
        ),
        pytest.param(
            "This is @em{not} a drill!",
            FragmentList(
                start_pos=0, end_pos=25,
                children=[
                    Text(
                        start_pos=0, end_pos=8,
                        inner="This is ",
                        enclosing=EnclosingPattern(left="", right=""),
                        at_prefix=False,
                    ),
                    Command(
                        start_pos=9, end_pos=16,
                        intro="em",
                        intro_enclosing=EnclosingPattern(left="", right=""),
                        options=None,
                        main_arg=FragmentList(
                            start_pos=12, end_pos=15,
                            children=[
                                Text(
                                    start_pos=12, end_pos=15,
                                    inner="not",
                                    enclosing=EnclosingPattern(left="", right=""),
                                    at_prefix=False,
                                ),
                            ],
                            enclosing=EnclosingPattern(left="{", right="}"),
                            at_prefix=False,
                        ),
                    ),
                    Text(
                        start_pos=16, end_pos=25,
                        inner=" a drill!",
                        enclosing=EnclosingPattern(left="", right=""),
                        at_prefix=False,
                    ),
                ],
                enclosing=GlobalEnclosingPattern(),
                at_prefix=False,
            ),
        ),
        pytest.param(
            '@|foo.process|{yes} @#|foo#process|#[@"no"]#"#"#',
            FragmentList(
                start_pos=0, end_pos=48,
                children=[
                    Command(
                        start_pos=1, end_pos=19,
                        intro="foo.process",
                        intro_enclosing=EnclosingPattern(left="|", right="|"),
                        options=None,
                        main_arg=FragmentList(
                            start_pos=15, end_pos=18,
                            children=[
                                Text(
                                    start_pos=15, end_pos=18,
                                    inner="yes",
                                    enclosing=EnclosingPattern(left="", right=""),
                                    at_prefix=False,
                                ),
                            ],
                            enclosing=EnclosingPattern(left="{", right="}"),
                            at_prefix=False,
                        ),
                    ),
                    Text(
                        start_pos=19, end_pos=20,
                        inner=" ",
                        enclosing=EnclosingPattern(left="", right=""),
                        at_prefix=False,
                    ),
                    Command(
                        start_pos=21, end_pos=48,
                        intro="foo#process",
                        intro_enclosing=EnclosingPattern(left="#|", right="|#"),
                        options=TokenList(
                            start_pos=37, end_pos=42,
                            children=[
                                Text(
                                    start_pos=39, end_pos=41,
                                    inner="no",
                                    enclosing=EnclosingPattern(left='"', right='"'),
                                    at_prefix=True,
                                ),
                            ],
                        ),
                        main_arg=Text(
                            start_pos=45, end_pos=46,
                            inner="#",
                            enclosing=EnclosingPattern(left='#"', right='"#'),
                            at_prefix=False,
                        ),
                    ),
                ],
                enclosing=GlobalEnclosingPattern(),
                at_prefix=False,
            ),
        ),
        pytest.param(
            "Level 0 @level1{ @level2{ @level3 } }",
            FragmentList(
                start_pos=0, end_pos=37,
                children=[
                    Text(
                        start_pos=0, end_pos=8,
                        inner="Level 0 ",
                        enclosing=EnclosingPattern(left="", right=""),
                        at_prefix=False,
                    ),
                    Command(
                        start_pos=9, end_pos=37,
                        intro="level1",
                        intro_enclosing=EnclosingPattern(left="", right=""),
                        options=None,
                        main_arg=FragmentList(
                            start_pos=16, end_pos=36,
                            children=[
                                Text(
                                    start_pos=16, end_pos=17,
                                    inner=" ",
                                    enclosing=EnclosingPattern(left="", right=""),
                                    at_prefix=False,
                                ),
                                Command(
                                    start_pos=18, end_pos=35,
                                    intro="level2",
                                    intro_enclosing=EnclosingPattern(left="", right=""),
                                    options=None,
                                    main_arg=FragmentList(
                                        start_pos=25, end_pos=34,
                                        children=[
                                            Text(
                                                start_pos=25, end_pos=26,
                                                inner=" ",
                                                enclosing=EnclosingPattern(
                                                    left="", right="",
                                                ),
                                                at_prefix=False,
                                            ),
                                            Command(
                                                start_pos=27, end_pos=33,
                                                intro="level3",
                                                intro_enclosing=EnclosingPattern(
                                                    left="", right="",
                                                ),
                                                options=None,
                                                main_arg=None,
                                            ),
                                            Text(
                                                start_pos=33, end_pos=34,
                                                inner=" ",
                                                enclosing=EnclosingPattern(
                                                    left="", right="",
                                                ),
                                                at_prefix=False,
                                            ),
                                        ],
                                        enclosing=EnclosingPattern(left="{", right="}"),
                                        at_prefix=False,
                                    ),
                                ),
                                Text(
                                    start_pos=35, end_pos=36,
                                    inner=" ",
                                    enclosing=EnclosingPattern(left="", right=""),
                                    at_prefix=False,
                                ),
                            ],
                            enclosing=EnclosingPattern(left="{", right="}"),
                            at_prefix=False,
                        ),
                    ),
                ],
                enclosing=GlobalEnclosingPattern(),
                at_prefix=False,
            ),
        ),
        pytest.param(
            '@say[greet=@"hello"]{John} at @email##"john@example.com"##!',
            FragmentList(
                start_pos=0, end_pos=59,
                children=[
                    Command(
                        start_pos=1, end_pos=26,
                        intro="say",
                        intro_enclosing=EnclosingPattern(left="", right=""),
                        options=TokenList(
                            start_pos=5, end_pos=19,
                            children=[
                                Identifier(start_pos=5, end_pos=10, name="greet"),
                                Operator(start_pos=10, end_pos=11, symbols="="),
                                Text(
                                    start_pos=13, end_pos=18,
                                    inner="hello",
                                    enclosing=EnclosingPattern(left='"', right='"'),
                                    at_prefix=True,
                                ),
                            ],
                        ),
                        main_arg=FragmentList(
                            start_pos=21, end_pos=25,
                            children=[
                                Text(
                                    start_pos=21, end_pos=25,
                                    inner="John",
                                    enclosing=EnclosingPattern(left="", right=""),
                                    at_prefix=False,
                                ),
                            ],
                            enclosing=EnclosingPattern(left="{", right="}"),
                            at_prefix=False,
                        ),
                    ),
                    Text(
                        start_pos=26, end_pos=30,
                        inner=" at ",
                        enclosing=EnclosingPattern(left="", right=""),
                        at_prefix=False,
                    ),
                    Command(
                        start_pos=31, end_pos=58,
                        intro="email",
                        intro_enclosing=EnclosingPattern(left="", right=""),
                        options=None,
                        main_arg=Text(
                            start_pos=39, end_pos=55,
                            inner="john@example.com",
                            enclosing=EnclosingPattern(left='##"', right='"##'),
                            at_prefix=False,
                        ),
                    ),
                    Text(
                        start_pos=58, end_pos=59,
                        inner="!",
                        enclosing=EnclosingPattern(left="", right=""),
                        at_prefix=False,
                    ),
                ],
                enclosing=GlobalEnclosingPattern(),
                at_prefix=False,
            ),
        ),
        pytest.param(
            '@###|state|###[x=1] @state[x=2]',
            FragmentList(
                start_pos=0, end_pos=31,
                children=[
                    Command(
                        start_pos=1, end_pos=19,
                        intro="state",
                        intro_enclosing=EnclosingPattern(left="###|", right="|###"),
                        options=TokenList(
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
                        at_prefix=False,
                    ),
                    Command(
                        start_pos=21, end_pos=31,
                        intro="state",
                        intro_enclosing=EnclosingPattern(left="", right=""),
                        options=TokenList(
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
                at_prefix=False,
            ),
        ),
        pytest.param(
            '@state[x=1,y=2,z=3]#"This symbol " is a quote!"#',
            FragmentList(
                start_pos=0, end_pos=48,
                children=[
                    Command(
                        start_pos=1, end_pos=48,
                        intro="state",
                        intro_enclosing=EnclosingPattern(left="", right=""),
                        options=TokenList(
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
                            at_prefix=False,
                        ),
                    ),
                ],
                enclosing=GlobalEnclosingPattern(),
                at_prefix=False,
            ),
        ),
        pytest.param(
            '@"@a @|1 + 1|", @|@name{} @"John"|, @say"cheese not @name"',
            FragmentList(
                start_pos=0, end_pos=58,
                children=[
                    Text(
                        start_pos=2, end_pos=13,
                        inner="@a @|1 + 1|",
                        enclosing=EnclosingPattern(left='"', right='"'),
                        at_prefix=True,
                    ),
                    Text(
                        start_pos=14, end_pos=16,
                        inner=", ",
                        enclosing=EnclosingPattern(left="", right=""),
                        at_prefix=False,
                    ),
                    Command(
                        start_pos=17, end_pos=34,
                        intro='@name{} @"John"',
                        intro_enclosing=EnclosingPattern(left="|", right="|"),
                        options=None,
                        main_arg=None,
                    ),
                    Text(
                        start_pos=34, end_pos=36,
                        inner=", ",
                        enclosing=EnclosingPattern(left="", right=""),
                        at_prefix=False,
                    ),
                    Command(
                        start_pos=37, end_pos=58,
                        intro="say",
                        intro_enclosing=EnclosingPattern(left="", right=""),
                        options=None,
                        main_arg=Text(
                            start_pos=41, end_pos=57,
                            inner="cheese not @name",
                            enclosing=EnclosingPattern(left='"', right='"'),
                            at_prefix=False,
                        ),
                    ),
                ],
                enclosing=GlobalEnclosingPattern(),
                at_prefix=False,
            ),
        ),
        pytest.param(
            '@|| @{} @"" @#||# @#{}# @##""##',
            FragmentList(
                start_pos=0,
                end_pos=31,
                children=[
                    Command(
                        start_pos=1, end_pos=3,
                        intro="",
                        intro_enclosing=EnclosingPattern(left="|", right="|"),
                        options=None,
                        main_arg=None,
                    ),
                    Text(
                        start_pos=3, end_pos=4,
                        inner=" ",
                        enclosing=EnclosingPattern(left="", right=""),
                        at_prefix=False,
                    ),
                    FragmentList(
                        start_pos=6, end_pos=6,
                        children=[],
                        enclosing=EnclosingPattern(left="{", right="}"),
                        at_prefix=True,
                    ),
                    Text(
                        start_pos=7, end_pos=8,
                        inner=" ",
                        enclosing=EnclosingPattern(left="", right=""),
                        at_prefix=False,
                    ),
                    Text(
                        start_pos=10, end_pos=10,
                        inner="",
                        enclosing=EnclosingPattern(left='"', right='"'),
                        at_prefix=True,
                    ),
                    Text(
                        start_pos=11, end_pos=12,
                        inner=" ",
                        enclosing=EnclosingPattern(left="", right=""),
                        at_prefix=False,
                    ),
                    Command(
                        start_pos=13, end_pos=17,
                        intro="",
                        intro_enclosing=EnclosingPattern(left="#|", right="|#"),
                        options=None,
                        main_arg=None,
                    ),
                    Text(
                        start_pos=17, end_pos=18,
                        inner=" ",
                        enclosing=EnclosingPattern(left="", right=""),
                        at_prefix=False,
                    ),
                    FragmentList(
                        start_pos=21, end_pos=21,
                        children=[],
                        enclosing=EnclosingPattern(left="#{", right="}#"),
                        at_prefix=True,
                    ),
                    Text(
                        start_pos=23, end_pos=24,
                        inner=" ",
                        enclosing=EnclosingPattern(left="", right=""),
                        at_prefix=False,
                    ),
                    Text(
                        start_pos=28, end_pos=28,
                        inner="",
                        enclosing=EnclosingPattern(left='##"', right='"##'),
                        at_prefix=True,
                    ),
                ],
                enclosing=GlobalEnclosingPattern(),
                at_prefix=False,
            ),
        ),
        pytest.param(
            '@foo[bar = @"x" + @|foo|[bar=@{x}|>3]]',
            FragmentList(
                start_pos=0, end_pos=38,
                children=[
                    Command(
                        start_pos=1, end_pos=38,
                        intro="foo",
                        intro_enclosing=EnclosingPattern(left="", right=""),
                        options=TokenList(
                            start_pos=5, end_pos=37,
                            children=[
                                Identifier(start_pos=5, end_pos=8, name="bar"),
                                Operator(start_pos=9, end_pos=10, symbols="="),
                                Text(
                                    start_pos=13, end_pos=14,
                                    inner="x",
                                    enclosing=EnclosingPattern(left='"', right='"'),
                                    at_prefix=True,
                                ),
                                Operator(start_pos=16, end_pos=17, symbols="+"),
                                Command(
                                    start_pos=19, end_pos=37,
                                    intro="foo",
                                    intro_enclosing=EnclosingPattern(
                                        left="|", right="|",
                                    ),
                                    options=TokenList(
                                        start_pos=25, end_pos=36,
                                        children=[
                                            Identifier(
                                                start_pos=25, end_pos=28, name="bar",
                                            ),
                                            Operator(
                                                start_pos=28, end_pos=29, symbols="=",
                                            ),
                                            FragmentList(
                                                start_pos=31, end_pos=32,
                                                children=[
                                                    Text(
                                                        start_pos=31, end_pos=32,
                                                        inner="x",
                                                        enclosing=EnclosingPattern(
                                                            left="", right="",
                                                        ),
                                                        at_prefix=False,
                                                    ),
                                                ],
                                                enclosing=EnclosingPattern(
                                                    left="{", right="}",
                                                ),
                                                at_prefix=True,
                                            ),
                                            Operator(
                                                start_pos=33, end_pos=35, symbols="|>",
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
                at_prefix=False,
            ),
        ),
        pytest.param(
            '@{@{@expand[1->2,<-3,stop,@"foo",,@|cool.fm|]{@|4+4|}}}',
            FragmentList(
                start_pos=0, end_pos=55,
                children=[
                    FragmentList(
                        start_pos=2, end_pos=54,
                        children=[
                            FragmentList(
                                start_pos=4, end_pos=53,
                                children=[
                                    Command(
                                        start_pos=5, end_pos=53,
                                        intro="expand",
                                        intro_enclosing=EnclosingPattern(left="",
                                                                         right=""),
                                        options=TokenList(
                                            start_pos=12, end_pos=44,
                                            children=[
                                                Number(start_pos=12, end_pos=13,
                                                       value=1),
                                                Operator(start_pos=13, end_pos=15,
                                                         symbols="->"),
                                                Number(start_pos=15, end_pos=16,
                                                       value=2),
                                                Operator(start_pos=16, end_pos=17,
                                                         symbols=","),
                                                Operator(start_pos=17, end_pos=19,
                                                         symbols="<-"),
                                                Number(start_pos=19, end_pos=20,
                                                       value=3),
                                                Operator(start_pos=20, end_pos=21,
                                                         symbols=","),
                                                Identifier(start_pos=21, end_pos=25,
                                                           name="stop"),
                                                Operator(start_pos=25, end_pos=26,
                                                         symbols=","),
                                                Text(
                                                    start_pos=28, end_pos=31,
                                                    inner="foo",
                                                    enclosing=EnclosingPattern(
                                                        left='"', right='"',
                                                    ),
                                                    at_prefix=True,
                                                ),
                                                Operator(start_pos=32, end_pos=33,
                                                         symbols=","),
                                                Operator(start_pos=33, end_pos=34,
                                                         symbols=","),
                                                Command(
                                                    start_pos=35, end_pos=44,
                                                    intro="cool.fm",
                                                    intro_enclosing=EnclosingPattern(
                                                        left="|", right="|",
                                                    ),
                                                    options=None,
                                                    main_arg=None,
                                                ),
                                            ],
                                        ),
                                        main_arg=FragmentList(
                                            start_pos=46, end_pos=52,
                                            children=[
                                                Command(
                                                    start_pos=47, end_pos=52,
                                                    intro="4+4",
                                                    intro_enclosing=EnclosingPattern(
                                                        left="|", right="|",
                                                    ),
                                                    options=None,
                                                    main_arg=None,
                                                ),
                                            ],
                                            enclosing=EnclosingPattern(
                                                left="{", right="}",
                                            ),
                                            at_prefix=False,
                                        ),
                                    ),
                                ],
                                enclosing=EnclosingPattern(left="{", right="}"),
                                at_prefix=True,
                            ),
                        ],
                        enclosing=EnclosingPattern(left="{", right="}"),
                        at_prefix=True,
                    ),
                ],
                enclosing=GlobalEnclosingPattern(),
                at_prefix=False,
            ),
        ),
        pytest.param(
            "@foo[()->(),{}->[],@||]",
            FragmentList(
                start_pos=0, end_pos=23,
                children=[
                    Command(
                        start_pos=1, end_pos=23,
                        intro="foo",
                        intro_enclosing=EnclosingPattern(left="", right=""),
                        options=TokenList(
                            start_pos=5, end_pos=22,
                            children=[
                                TokenList(start_pos=6, end_pos=6, children=[]),
                                Operator(start_pos=7, end_pos=9, symbols="->"),
                                TokenList(start_pos=10, end_pos=10, children=[]),
                                Operator(start_pos=11, end_pos=12, symbols=","),
                                TokenList(start_pos=13, end_pos=13, children=[]),
                                Operator(start_pos=14, end_pos=16, symbols="->"),
                                TokenList(start_pos=17, end_pos=17, children=[]),
                                Operator(start_pos=18, end_pos=19, symbols=","),
                                Command(
                                    start_pos=20, end_pos=22,
                                    intro="",
                                    intro_enclosing=EnclosingPattern(
                                        left="|", right="|",
                                    ),
                                    options=None,
                                    main_arg=None,
                                ),
                            ],
                        ),
                        main_arg=None,
                    ),
                ],
                enclosing=GlobalEnclosingPattern(),
                at_prefix=False,
            ),
        ),
        pytest.param(
            '@foo[\n  a = {1 -> 2},\n  b = @{My name is @name},\n]{bar}\n',
            FragmentList(
                start_pos=0, end_pos=56,
                children=[
                    Command(
                        start_pos=1, end_pos=55,
                        intro="foo",
                        intro_enclosing=EnclosingPattern(left="", right=""),
                        options=TokenList(
                            start_pos=5, end_pos=48,
                            children=[
                                Identifier(start_pos=8, end_pos=9, name="a"),
                                Operator(start_pos=10, end_pos=11, symbols="="),
                                TokenList(
                                    start_pos=13, end_pos=19,
                                    children=[
                                        Number(start_pos=13, end_pos=14, value=1),
                                        Operator(start_pos=15, end_pos=17,
                                                 symbols="->"),
                                        Number(start_pos=18, end_pos=19, value=2),
                                    ],
                                ),
                                Operator(start_pos=20, end_pos=21, symbols=","),
                                Identifier(start_pos=24, end_pos=25, name="b"),
                                Operator(start_pos=26, end_pos=27, symbols="="),
                                FragmentList(
                                    start_pos=30, end_pos=46,
                                    children=[
                                        Text(
                                            start_pos=30, end_pos=41,
                                            inner="My name is ",
                                            enclosing=EnclosingPattern(
                                                left="", right="",
                                            ),
                                            at_prefix=False,
                                        ),
                                        Command(
                                            start_pos=42, end_pos=46,
                                            intro="name",
                                            intro_enclosing=EnclosingPattern(
                                                left="", right="",
                                            ),
                                            options=None,
                                            main_arg=None,
                                        ),
                                    ],
                                    enclosing=EnclosingPattern(left="{", right="}"),
                                    at_prefix=True,
                                ),
                                Operator(start_pos=47, end_pos=48, symbols=","),
                            ],
                        ),
                        main_arg=FragmentList(
                            start_pos=51, end_pos=54,
                            children=[
                                Text(
                                    start_pos=51, end_pos=54,
                                    inner="bar",
                                    enclosing=EnclosingPattern(left="", right=""),
                                    at_prefix=False,
                                ),
                            ],
                            enclosing=EnclosingPattern(left="{", right="}"),
                            at_prefix=False,
                        ),
                    ),
                    Text(
                        start_pos=55, end_pos=56,
                        inner="\n",
                        enclosing=EnclosingPattern(left="", right=""),
                        at_prefix=False,
                    ),
                ],
                enclosing=GlobalEnclosingPattern(),
                at_prefix=False,
            ),
        ),
    ],
)
def test_parser(input_text: str, expected: Token):
    tree = ParseContext(input_text).tree
    assert tree == expected
    assert tree.start_pos == expected.start_pos
    assert tree.end_pos == expected.end_pos

# TODO: need to add a lot more unit tests
