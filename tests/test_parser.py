import pytest  # noqa

from paxter.core import (
    FragmentList, Identifier, Number, Operator, ParseContext, PaxterApply, PaxterPhrase,
    Text, Token, TokenList,
)
from paxter.core.scope_pattern import EMPTY_SCOPE_PATTERN, GLOBAL_SCOPE_PATTERN, \
    ScopePattern


@pytest.mark.parametrize(
    ("input_text", "expected"),
    [
        pytest.param(
            "",
            FragmentList(
                start_pos=0, end_pos=0,
                children=[],
                scope_pattern=GLOBAL_SCOPE_PATTERN,
                is_command=False,
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
                        scope_pattern=EMPTY_SCOPE_PATTERN,
                        is_command=False,
                    ),
                ],
                scope_pattern=GLOBAL_SCOPE_PATTERN,
                is_command=False,
            ),
        ),
        pytest.param(
            "@hello",
            FragmentList(
                start_pos=0, end_pos=6,
                children=[
                    PaxterPhrase(
                        start_pos=1, end_pos=6,
                        inner="hello",
                        scope_pattern=EMPTY_SCOPE_PATTERN,
                    ),
                ],
                scope_pattern=GLOBAL_SCOPE_PATTERN,
                is_command=False,
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
                        scope_pattern=EMPTY_SCOPE_PATTERN,
                        is_command=False,
                    ),
                    PaxterPhrase(
                        start_pos=19, end_pos=23,
                        inner="name",
                        scope_pattern=EMPTY_SCOPE_PATTERN,
                    ),
                    Text(
                        start_pos=23, end_pos=24,
                        inner=".",
                        scope_pattern=EMPTY_SCOPE_PATTERN,
                        is_command=False,
                    ),
                ],
                scope_pattern=GLOBAL_SCOPE_PATTERN,
                is_command=False,
            ),
        ),
        pytest.param(
            "The result of 1 + 1 is @|1 + 1|. Yes! @<#|1 + 1|#>",
            FragmentList(
                start_pos=0, end_pos=50,
                children=[
                    Text(
                        start_pos=0, end_pos=23,
                        inner="The result of 1 + 1 is ",
                        scope_pattern=EMPTY_SCOPE_PATTERN,
                        is_command=False,
                    ),
                    PaxterPhrase(
                        start_pos=25, end_pos=30,
                        inner="1 + 1",
                        scope_pattern=ScopePattern(opening="|", closing="|"),
                    ),
                    Text(
                        start_pos=31, end_pos=38,
                        inner=". Yes! ",
                        scope_pattern=EMPTY_SCOPE_PATTERN,
                        is_command=False,
                    ),
                    PaxterPhrase(
                        start_pos=42, end_pos=47,
                        inner="1 + 1",
                        scope_pattern=ScopePattern(opening="<#|", closing="|#>"),
                    ),
                ],
                scope_pattern=GLOBAL_SCOPE_PATTERN,
                is_command=False,
            ),
        ),
        pytest.param(
            "@|N @ M @ K|",
            FragmentList(
                start_pos=0, end_pos=12,
                children=[
                    PaxterPhrase(
                        start_pos=2, end_pos=11,
                        inner="N @ M @ K",
                        scope_pattern=ScopePattern(opening="|", closing="|"),
                    ),
                ],
                scope_pattern=GLOBAL_SCOPE_PATTERN,
                is_command=False,
            ),
        ),
        pytest.param(
            "@<#|#|#|#>, @<<|<|>|>>, @@@,@;",
            FragmentList(
                start_pos=0, end_pos=30,
                children=[
                    PaxterPhrase(
                        start_pos=4, end_pos=7,
                        inner="#|#",
                        scope_pattern=ScopePattern(opening="<#|", closing="|#>"),
                    ),
                    Text(
                        start_pos=10,
                        end_pos=12,
                        inner=", ",
                        scope_pattern=EMPTY_SCOPE_PATTERN,
                        is_command=False,
                    ),
                    PaxterPhrase(
                        start_pos=16,
                        end_pos=19,
                        inner="<|>",
                        scope_pattern=ScopePattern(opening="<<|", closing="|>>"),
                    ),
                    Text(
                        start_pos=22,
                        end_pos=24,
                        inner=", ",
                        scope_pattern=EMPTY_SCOPE_PATTERN,
                        is_command=False,
                    ),
                    PaxterPhrase(
                        start_pos=25,
                        end_pos=26,
                        inner="@",
                        scope_pattern=EMPTY_SCOPE_PATTERN,
                    ),
                    PaxterPhrase(
                        start_pos=27,
                        end_pos=28,
                        inner=",",
                        scope_pattern=EMPTY_SCOPE_PATTERN,
                    ),
                    PaxterPhrase(
                        start_pos=29,
                        end_pos=30,
                        inner=";",
                        scope_pattern=EMPTY_SCOPE_PATTERN,
                    ),
                ],
                scope_pattern=GLOBAL_SCOPE_PATTERN,
                is_command=False,
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
                        scope_pattern=EMPTY_SCOPE_PATTERN,
                        is_command=False,
                    ),
                    PaxterApply(
                        start_pos=9, end_pos=16,
                        id=Identifier(start_pos=9, end_pos=11, name="em"),
                        options=None,
                        main_arg=FragmentList(
                            start_pos=12, end_pos=15,
                            children=[
                                Text(
                                    start_pos=12, end_pos=15,
                                    inner="not",
                                    scope_pattern=EMPTY_SCOPE_PATTERN,
                                    is_command=False,
                                ),
                            ],
                            scope_pattern=ScopePattern(opening="{", closing="}"),
                            is_command=False,
                        ),
                    ),
                    Text(
                        start_pos=16, end_pos=25,
                        inner=" a drill!",
                        scope_pattern=EMPTY_SCOPE_PATTERN,
                        is_command=False,
                    ),
                ],
                scope_pattern=GLOBAL_SCOPE_PATTERN,
                is_command=False,
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
                        scope_pattern=EMPTY_SCOPE_PATTERN,
                        is_command=False,
                    ),
                    PaxterApply(
                        start_pos=9, end_pos=37,
                        id=Identifier(start_pos=9, end_pos=15, name="level1"),
                        options=None,
                        main_arg=FragmentList(
                            start_pos=16, end_pos=36,
                            children=[
                                Text(
                                    start_pos=16, end_pos=17,
                                    inner=" ",
                                    scope_pattern=EMPTY_SCOPE_PATTERN,
                                    is_command=False,
                                ),
                                PaxterApply(
                                    start_pos=18, end_pos=35,
                                    id=Identifier(
                                        start_pos=18, end_pos=24,
                                        name="level2",
                                    ),
                                    options=None,
                                    main_arg=FragmentList(
                                        start_pos=25, end_pos=34,
                                        children=[
                                            Text(
                                                start_pos=25, end_pos=26,
                                                inner=" ",
                                                scope_pattern=EMPTY_SCOPE_PATTERN,
                                                is_command=False,
                                            ),
                                            PaxterPhrase(
                                                start_pos=27, end_pos=33,
                                                inner="level3",
                                                scope_pattern=EMPTY_SCOPE_PATTERN,
                                            ),
                                            Text(
                                                start_pos=33, end_pos=34,
                                                inner=" ",
                                                scope_pattern=EMPTY_SCOPE_PATTERN,
                                                is_command=False,
                                            ),
                                        ],
                                        scope_pattern=ScopePattern(
                                            opening="{", closing="}",
                                        ),
                                        is_command=False,
                                    ),
                                ),
                                Text(
                                    start_pos=35, end_pos=36,
                                    inner=" ",
                                    scope_pattern=EMPTY_SCOPE_PATTERN,
                                    is_command=False,
                                ),
                            ],
                            scope_pattern=ScopePattern(opening="{", closing="}"),
                            is_command=False,
                        ),
                    ),
                ],
                scope_pattern=GLOBAL_SCOPE_PATTERN,
                is_command=False,
            ),
        ),
        pytest.param(
            '@say[greet=@"hello"]{John} at @email<#"john@example.com"#>!',
            FragmentList(
                start_pos=0, end_pos=59,
                children=[
                    PaxterApply(
                        start_pos=1, end_pos=26,
                        id=Identifier(start_pos=1, end_pos=4, name="say"),
                        options=TokenList(
                            start_pos=5, end_pos=19,
                            children=[
                                Identifier(start_pos=5, end_pos=10, name="greet"),
                                Operator(start_pos=10, end_pos=11, symbol="="),
                                Text(
                                    start_pos=13, end_pos=18,
                                    inner="hello",
                                    scope_pattern=ScopePattern(opening='"',
                                                               closing='"'),
                                    is_command=True,
                                ),
                            ],
                        ),
                        main_arg=FragmentList(
                            start_pos=21, end_pos=25,
                            children=[
                                Text(
                                    start_pos=21, end_pos=25,
                                    inner="John",
                                    scope_pattern=EMPTY_SCOPE_PATTERN,
                                    is_command=False,
                                ),
                            ],
                            scope_pattern=ScopePattern(opening="{", closing="}"),
                            is_command=False,
                        ),
                    ),
                    Text(
                        start_pos=26, end_pos=30,
                        inner=" at ",
                        scope_pattern=EMPTY_SCOPE_PATTERN,
                        is_command=False,
                    ),
                    PaxterApply(
                        start_pos=31, end_pos=58,
                        id=Identifier(start_pos=31, end_pos=36, name="email"),
                        options=None,
                        main_arg=Text(
                            start_pos=39, end_pos=55,
                            inner="john@example.com",
                            scope_pattern=ScopePattern(opening='<#"', closing='"#>'),
                            is_command=False,
                        ),
                    ),
                    Text(
                        start_pos=58, end_pos=59,
                        inner="!",
                        scope_pattern=EMPTY_SCOPE_PATTERN,
                        is_command=False,
                    ),
                ],
                scope_pattern=GLOBAL_SCOPE_PATTERN,
                is_command=False,
            ),
        ),
        pytest.param(
            '@state[x=1]',
            FragmentList(
                start_pos=0, end_pos=11,
                children=[
                    PaxterApply(
                        start_pos=1, end_pos=11,
                        id=Identifier(start_pos=1, end_pos=6, name="state"),
                        options=TokenList(
                            start_pos=7, end_pos=10,
                            children=[
                                Identifier(start_pos=7, end_pos=8, name="x"),
                                Operator(start_pos=8, end_pos=9, symbol="="),
                                Number(start_pos=9, end_pos=10, value=1),
                            ],
                        ),
                        main_arg=None,
                    ),
                ],
                scope_pattern=GLOBAL_SCOPE_PATTERN,
                is_command=False,
            ),
        ),
        pytest.param(
            '@state[x=1,y=2,z=3]#"This symbol " is a quote!"#',
            FragmentList(
                start_pos=0, end_pos=48,
                children=[
                    PaxterApply(
                        start_pos=1, end_pos=48,
                        id=Identifier(start_pos=1, end_pos=6, name="state"),
                        options=TokenList(
                            start_pos=7, end_pos=18,
                            children=[
                                Identifier(start_pos=7, end_pos=8, name="x"),
                                Operator(start_pos=8, end_pos=9, symbol="="),
                                Number(start_pos=9, end_pos=10, value=1),
                                Operator(start_pos=10, end_pos=11, symbol=","),
                                Identifier(start_pos=11, end_pos=12, name="y"),
                                Operator(start_pos=12, end_pos=13, symbol="="),
                                Number(start_pos=13, end_pos=14, value=2),
                                Operator(start_pos=14, end_pos=15, symbol=","),
                                Identifier(start_pos=15, end_pos=16, name="z"),
                                Operator(start_pos=16, end_pos=17, symbol="="),
                                Number(start_pos=17, end_pos=18, value=3),
                            ],
                        ),
                        main_arg=Text(
                            start_pos=21, end_pos=46,
                            inner='This symbol " is a quote!',
                            scope_pattern=ScopePattern(opening='#"', closing='"#'),
                            is_command=False,
                        ),
                    ),
                ],
                scope_pattern=GLOBAL_SCOPE_PATTERN,
                is_command=False,
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
                        scope_pattern=ScopePattern(opening='"', closing='"'),
                        is_command=True,
                    ),
                    Text(
                        start_pos=14, end_pos=16,
                        inner=", ",
                        scope_pattern=EMPTY_SCOPE_PATTERN,
                        is_command=False,
                    ),
                    PaxterPhrase(
                        start_pos=18, end_pos=33,
                        inner='@name{} @"John"',
                        scope_pattern=ScopePattern(opening="|", closing="|"),
                    ),
                    Text(
                        start_pos=34, end_pos=36,
                        inner=", ",
                        scope_pattern=EMPTY_SCOPE_PATTERN,
                        is_command=False,
                    ),
                    PaxterApply(
                        start_pos=37, end_pos=58,
                        id=Identifier(start_pos=37, end_pos=40, name="say"),
                        options=None,
                        main_arg=Text(
                            start_pos=41,
                            end_pos=57,
                            inner="cheese not @name",
                            scope_pattern=ScopePattern(opening='"', closing='"'),
                            is_command=False,
                        ),
                    ),
                ],
                scope_pattern=GLOBAL_SCOPE_PATTERN,
                is_command=False,
            ),
        ),
        pytest.param(
            '@|| @{} @"" @#||# @<{}> @<#""#>',
            FragmentList(
                start_pos=0, end_pos=31,
                children=[
                    PaxterPhrase(
                        start_pos=2, end_pos=2,
                        inner="",
                        scope_pattern=ScopePattern(opening="|", closing="|"),
                    ),
                    Text(
                        start_pos=3, end_pos=4,
                        inner=" ",
                        scope_pattern=EMPTY_SCOPE_PATTERN,
                        is_command=False,
                    ),
                    FragmentList(
                        start_pos=6, end_pos=6,
                        children=[],
                        scope_pattern=ScopePattern(opening="{", closing="}"),
                        is_command=True,
                    ),
                    Text(
                        start_pos=7, end_pos=8,
                        inner=" ",
                        scope_pattern=EMPTY_SCOPE_PATTERN,
                        is_command=False,
                    ),
                    Text(
                        start_pos=10, end_pos=10,
                        inner="",
                        scope_pattern=ScopePattern(opening='"', closing='"'),
                        is_command=True,
                    ),
                    Text(
                        start_pos=11, end_pos=12,
                        inner=" ",
                        scope_pattern=EMPTY_SCOPE_PATTERN,
                        is_command=False,
                    ),
                    PaxterPhrase(
                        start_pos=15, end_pos=15,
                        inner="",
                        scope_pattern=ScopePattern(opening="#|", closing="|#"),
                    ),
                    Text(
                        start_pos=17, end_pos=18,
                        inner=" ",
                        scope_pattern=EMPTY_SCOPE_PATTERN,
                        is_command=False,
                    ),
                    FragmentList(
                        start_pos=21, end_pos=21,
                        children=[],
                        scope_pattern=ScopePattern(opening="<{", closing="}>"),
                        is_command=True,
                    ),
                    Text(
                        start_pos=23, end_pos=24,
                        inner=" ",
                        scope_pattern=EMPTY_SCOPE_PATTERN,
                        is_command=False,
                    ),
                    Text(
                        start_pos=28, end_pos=28,
                        inner="",
                        scope_pattern=ScopePattern(opening='<#"', closing='"#>'),
                        is_command=True,
                    ),
                ],
                scope_pattern=GLOBAL_SCOPE_PATTERN,
                is_command=False,
            ),
        ),
        pytest.param(
            '@foo[bar = @"x" + @foo[bar=@{x}|>3]]',
            FragmentList(
                start_pos=0, end_pos=36,
                children=[
                    PaxterApply(
                        start_pos=1, end_pos=36,
                        id=Identifier(start_pos=1, end_pos=4, name="foo"),
                        options=TokenList(
                            start_pos=5, end_pos=35,
                            children=[
                                Identifier(start_pos=5, end_pos=8, name="bar"),
                                Operator(start_pos=9, end_pos=10, symbol="="),
                                Text(
                                    start_pos=13, end_pos=14,
                                    inner="x",
                                    scope_pattern=ScopePattern(opening='"',
                                                               closing='"'),
                                    is_command=True,
                                ),
                                Operator(start_pos=16, end_pos=17, symbol="+"),
                                PaxterApply(
                                    start_pos=19, end_pos=35,
                                    id=Identifier(start_pos=19, end_pos=22, name="foo"),
                                    options=TokenList(
                                        start_pos=23, end_pos=34,
                                        children=[
                                            Identifier(
                                                start_pos=23, end_pos=26,
                                                name="bar",
                                            ),
                                            Operator(
                                                start_pos=26, end_pos=27,
                                                symbol="=",
                                            ),
                                            FragmentList(
                                                start_pos=29, end_pos=30,
                                                children=[
                                                    Text(
                                                        start_pos=29, end_pos=30,
                                                        inner="x",
                                                        scope_pattern=(
                                                                EMPTY_SCOPE_PATTERN
                                                        ),
                                                        is_command=False,
                                                    ),
                                                ],
                                                scope_pattern=ScopePattern(
                                                    opening="{", closing="}",
                                                ),
                                                is_command=True,
                                            ),
                                            Operator(
                                                start_pos=31, end_pos=33,
                                                symbol="|>",
                                            ),
                                            Number(start_pos=33, end_pos=34, value=3),
                                        ],
                                    ),
                                    main_arg=None,
                                ),
                            ],
                        ),
                        main_arg=None,
                    ),
                ],
                scope_pattern=GLOBAL_SCOPE_PATTERN,
                is_command=False,
            ),
        ),
        pytest.param(
            '@{@{@expand[1->2,<-3,stop,@"foo",,@cool]{@|4+4|}}}',
            FragmentList(
                start_pos=0, end_pos=50,
                children=[
                    FragmentList(
                        start_pos=2, end_pos=49,
                        children=[
                            FragmentList(
                                start_pos=4, end_pos=48,
                                children=[
                                    PaxterApply(
                                        start_pos=5, end_pos=48,
                                        id=Identifier(
                                            start_pos=5, end_pos=11,
                                            name="expand",
                                        ),
                                        options=TokenList(
                                            start_pos=12, end_pos=39,
                                            children=[
                                                Number(
                                                    start_pos=12, end_pos=13,
                                                    value=1,
                                                ),
                                                Operator(
                                                    start_pos=13, end_pos=15,
                                                    symbol="->",
                                                ),
                                                Number(
                                                    start_pos=15, end_pos=16,
                                                    value=2,
                                                ),
                                                Operator(
                                                    start_pos=16, end_pos=17,
                                                    symbol=",",
                                                ),
                                                Operator(
                                                    start_pos=17, end_pos=19,
                                                    symbol="<-",
                                                ),
                                                Number(
                                                    start_pos=19, end_pos=20,
                                                    value=3,
                                                ),
                                                Operator(
                                                    start_pos=20, end_pos=21,
                                                    symbol=",",
                                                ),
                                                Identifier(
                                                    start_pos=21, end_pos=25,
                                                    name="stop",
                                                ),
                                                Operator(
                                                    start_pos=25, end_pos=26,
                                                    symbol=",",
                                                ),
                                                Text(
                                                    start_pos=28, end_pos=31,
                                                    inner="foo",
                                                    scope_pattern=ScopePattern(
                                                        opening='"', closing='"',
                                                    ),
                                                    is_command=True,
                                                ),
                                                Operator(
                                                    start_pos=32, end_pos=33,
                                                    symbol=",",
                                                ),
                                                Operator(
                                                    start_pos=33, end_pos=34,
                                                    symbol=",",
                                                ),
                                                PaxterPhrase(
                                                    start_pos=35, end_pos=39,
                                                    inner="cool",
                                                    scope_pattern=EMPTY_SCOPE_PATTERN,
                                                ),
                                            ],
                                        ),
                                        main_arg=FragmentList(
                                            start_pos=41, end_pos=47,
                                            children=[
                                                PaxterPhrase(
                                                    start_pos=43, end_pos=46,
                                                    inner="4+4",
                                                    scope_pattern=ScopePattern(
                                                        opening="|", closing="|",
                                                    ),
                                                ),
                                            ],
                                            scope_pattern=ScopePattern(
                                                opening="{", closing="}",
                                            ),
                                            is_command=False,
                                        ),
                                    ),
                                ],
                                scope_pattern=ScopePattern(opening="{", closing="}"),
                                is_command=True,
                            ),
                        ],
                        scope_pattern=ScopePattern(opening="{", closing="}"),
                        is_command=True,
                    ),
                ],
                scope_pattern=GLOBAL_SCOPE_PATTERN,
                is_command=False,
            ),
        ),
        pytest.param(
            "@foo[()->(),{}->[]]",
            FragmentList(
                start_pos=0, end_pos=19,
                children=[
                    PaxterApply(
                        start_pos=1, end_pos=19,
                        id=Identifier(start_pos=1, end_pos=4, name="foo"),
                        options=TokenList(
                            start_pos=5, end_pos=18,
                            children=[
                                TokenList(start_pos=6, end_pos=6, children=[]),
                                Operator(start_pos=7, end_pos=9, symbol="->"),
                                TokenList(start_pos=10, end_pos=10, children=[]),
                                Operator(start_pos=11, end_pos=12, symbol=","),
                                TokenList(start_pos=13, end_pos=13, children=[]),
                                Operator(start_pos=14, end_pos=16, symbol="->"),
                                TokenList(start_pos=17, end_pos=17, children=[]),
                            ],
                        ),
                        main_arg=None,
                    ),
                ],
                scope_pattern=GLOBAL_SCOPE_PATTERN,
                is_command=False,
            ),
        ),
        pytest.param(
            '@foo[\n'
            '  a = {1 -> 2},\n'
            '  b = @{My name is @name},\n'
            ']{bar}\n',
            FragmentList(
                start_pos=0, end_pos=56,
                children=[
                    PaxterApply(
                        start_pos=1, end_pos=55,
                        id=Identifier(start_pos=1, end_pos=4, name="foo"),
                        options=TokenList(
                            start_pos=5, end_pos=48,
                            children=[
                                Identifier(start_pos=8, end_pos=9, name="a"),
                                Operator(start_pos=10, end_pos=11, symbol="="),
                                TokenList(
                                    start_pos=13, end_pos=19,
                                    children=[
                                        Number(start_pos=13, end_pos=14, value=1),
                                        Operator(start_pos=15, end_pos=17, symbol="->"),
                                        Number(start_pos=18, end_pos=19, value=2),
                                    ],
                                ),
                                Operator(start_pos=20, end_pos=21, symbol=","),
                                Identifier(start_pos=24, end_pos=25, name="b"),
                                Operator(start_pos=26, end_pos=27, symbol="="),
                                FragmentList(
                                    start_pos=30, end_pos=46,
                                    children=[
                                        Text(
                                            start_pos=30,
                                            end_pos=41,
                                            inner="My name is ",
                                            scope_pattern=EMPTY_SCOPE_PATTERN,
                                            is_command=False,
                                        ),
                                        PaxterPhrase(
                                            start_pos=42,
                                            end_pos=46,
                                            inner="name",
                                            scope_pattern=EMPTY_SCOPE_PATTERN,
                                        ),
                                    ],
                                    scope_pattern=ScopePattern(opening="{",
                                                               closing="}"),
                                    is_command=True,
                                ),
                                Operator(start_pos=47, end_pos=48, symbol=","),
                            ],
                        ),
                        main_arg=FragmentList(
                            start_pos=51, end_pos=54,
                            children=[
                                Text(
                                    start_pos=51, end_pos=54,
                                    inner="bar",
                                    scope_pattern=EMPTY_SCOPE_PATTERN,
                                    is_command=False,
                                ),
                            ],
                            scope_pattern=ScopePattern(opening="{", closing="}"),
                            is_command=False,
                        ),
                    ),
                    Text(
                        start_pos=55, end_pos=56,
                        inner="\n",
                        scope_pattern=EMPTY_SCOPE_PATTERN,
                        is_command=False,
                    ),
                ],
                scope_pattern=GLOBAL_SCOPE_PATTERN,
                is_command=False,
            ),
        ),
    ],
)
def test_parser(input_text: str, expected: Token):
    tree = ParseContext(input_text).parse()
    assert tree == expected
    assert tree.start_pos == expected.start_pos
    assert tree.end_pos == expected.end_pos

# TODO: need to add a lot more unit tests
