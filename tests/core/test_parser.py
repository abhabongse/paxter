import pytest

from paxter.core import (FragmentList, Identifier, Parser, PaxterFunc, PaxterMacro,
                         PaxterPhrase, Text)


# TODO: add more unit tests for syntax errors

@pytest.mark.parametrize(
    ("input_text", "expected"),
    [
        pytest.param(
            " @hello{ @hi{x} }>",
            FragmentList(
                start_pos=0, end_pos=18,
                children=[
                    Text(start_pos=0, end_pos=1, string=" "),
                    PaxterFunc(
                        start_pos=1, end_pos=17,
                        id=Identifier(start_pos=2, end_pos=7, name="hello"),
                        fragments=FragmentList(
                            start_pos=8, end_pos=16,
                            children=[
                                Text(start_pos=8, end_pos=9, string=" "),
                                PaxterFunc(
                                    start_pos=9, end_pos=15,
                                    id=Identifier(start_pos=10, end_pos=12, name="hi"),
                                    fragments=FragmentList(
                                        start_pos=13, end_pos=14,
                                        children=[
                                            Text(start_pos=13, end_pos=14, string="x"),
                                        ],
                                    ),
                                    options=None,
                                ),
                                Text(start_pos=15, end_pos=16, string=" "),
                            ],
                        ),
                        options=None,
                    ),
                    Text(start_pos=17, end_pos=18, string=">"),
                ],
            ),
        ),
        pytest.param(
            "@yes{!@{x}_@y^@z{1}_}",
            FragmentList(
                start_pos=0, end_pos=21,
                children=[
                    PaxterFunc(
                        start_pos=0, end_pos=21,
                        id=Identifier(start_pos=1, end_pos=4, name="yes"),
                        fragments=FragmentList(
                            start_pos=5, end_pos=20,
                            children=[
                                Text(start_pos=5, end_pos=6, string="!"),
                                PaxterPhrase(
                                    start_pos=6, end_pos=10,
                                    phrase=Text(start_pos=8, end_pos=9, string="x"),
                                ),
                                Text(start_pos=10, end_pos=11, string="_"),
                                PaxterPhrase(
                                    start_pos=11, end_pos=13,
                                    phrase=Text(start_pos=12, end_pos=13, string="y"),
                                ),
                                Text(start_pos=13, end_pos=14, string="^"),
                                PaxterFunc(
                                    start_pos=14, end_pos=19,
                                    id=Identifier(start_pos=15, end_pos=16, name="z"),
                                    fragments=FragmentList(
                                        start_pos=17, end_pos=18,
                                        children=[
                                            Text(start_pos=17, end_pos=18, string="1"),
                                        ],
                                    ),
                                    options=None,
                                ),
                                Text(start_pos=19, end_pos=20, string="_"),
                            ],
                        ),
                        options=None,
                    ),
                ],
            ),
        ),
        pytest.param(
            " @hello<{{}}>",
            FragmentList(
                start_pos=0, end_pos=13,
                children=[
                    Text(start_pos=0, end_pos=1, string=" "),
                    PaxterFunc(
                        start_pos=1, end_pos=13,
                        id=Identifier(start_pos=2, end_pos=7, name="hello"),
                        fragments=FragmentList(
                            start_pos=9, end_pos=11,
                            children=[Text(start_pos=9, end_pos=11, string="{}")],
                        ),
                        options=None,
                    ),
                ],
            ),
        ),
        pytest.param(
            " @hey!{@>@} ",
            FragmentList(
                start_pos=0, end_pos=12,
                children=[
                    Text(start_pos=0, end_pos=1, string=" "),
                    PaxterMacro(
                        start_pos=1, end_pos=11,
                        id=Identifier(start_pos=2, end_pos=6, name="hey!"),
                        text=Text(start_pos=7, end_pos=10, string="@>@"),
                    ),
                    Text(start_pos=11, end_pos=12, string=" "),
                ],
            ),
        ),
        pytest.param(
            "@!{@hello{}}",
            FragmentList(
                start_pos=0, end_pos=12,
                children=[
                    PaxterMacro(
                        start_pos=0, end_pos=11,
                        id=Identifier(start_pos=1, end_pos=2, name="!"),
                        text=Text(start_pos=3, end_pos=10, string="@hello{"),
                    ),
                    Text(start_pos=11, end_pos=12, string="}"),
                ],
            ),
        ),
        pytest.param(
            "@!#{@hello{}}#",
            FragmentList(
                start_pos=0, end_pos=14,
                children=[
                    PaxterMacro(
                        start_pos=0, end_pos=14,
                        id=Identifier(start_pos=1, end_pos=2, name="!"),
                        text=Text(start_pos=4, end_pos=12, string="@hello{}"),
                    ),
                ],
            ),
        ),
        pytest.param(
            "@hello{@hi}",
            FragmentList(
                start_pos=0, end_pos=11,
                children=[
                    PaxterFunc(
                        start_pos=0, end_pos=11,
                        id=Identifier(start_pos=1, end_pos=6, name="hello"),
                        fragments=FragmentList(
                            start_pos=7, end_pos=10,
                            children=[
                                PaxterPhrase(
                                    start_pos=7, end_pos=10,
                                    phrase=Text(start_pos=8, end_pos=10, string="hi"),
                                ),
                            ],
                        ),
                        options=None,
                    ),
                ],
            ),
        ),
        pytest.param(
            r'\@"\@"',
            FragmentList(
                start_pos=0, end_pos=6,
                children=[
                    Text(start_pos=0, end_pos=1, string="\\"),
                    Text(start_pos=1, end_pos=6, string="\\@"),
                ],
            ),
        ),
        pytest.param(
            r'Hello @good boy @{good} boy @<{good boy}>',
            FragmentList(
                start_pos=0, end_pos=41,
                children=[
                    Text(start_pos=0, end_pos=6, string="Hello "),
                    PaxterPhrase(
                        start_pos=6, end_pos=11,
                        phrase=Text(start_pos=7, end_pos=11, string="good"),
                    ),
                    Text(start_pos=11, end_pos=16, string=" boy "),
                    PaxterPhrase(
                        start_pos=16, end_pos=23,
                        phrase=Text(start_pos=18, end_pos=22, string="good"),
                    ),
                    Text(start_pos=23, end_pos=28, string=" boy "),
                    PaxterPhrase(
                        start_pos=28, end_pos=41,
                        phrase=Text(start_pos=31, end_pos=39, string="good boy"),
                    ),
                ],
            ),
        ),
        pytest.param(
            r'@hello{@hello#{@hello<{@hello and {}}>{}}#}',
            FragmentList(
                start_pos=0, end_pos=43,
                children=[
                    PaxterFunc(
                        start_pos=0, end_pos=43,
                        id=Identifier(start_pos=1, end_pos=6, name="hello"),
                        fragments=FragmentList(
                            start_pos=7, end_pos=42,
                            children=[
                                PaxterFunc(
                                    start_pos=7, end_pos=42,
                                    id=Identifier(
                                        start_pos=8, end_pos=13,
                                        name="hello",
                                    ),
                                    fragments=FragmentList(
                                        start_pos=15, end_pos=40,
                                        children=[
                                            PaxterFunc(
                                                start_pos=15, end_pos=38,
                                                id=Identifier(
                                                    start_pos=16, end_pos=21,
                                                    name="hello",
                                                ),
                                                fragments=FragmentList(
                                                    start_pos=23,
                                                    end_pos=36,
                                                    children=[
                                                        PaxterPhrase(
                                                            start_pos=23,
                                                            end_pos=29,
                                                            phrase=Text(
                                                                start_pos=24,
                                                                end_pos=29,
                                                                string="hello",
                                                            ),
                                                        ),
                                                        Text(
                                                            start_pos=29, end_pos=36,
                                                            string=" and {}",
                                                        ),
                                                    ],
                                                ),
                                                options=None,
                                            ),
                                            Text(start_pos=38, end_pos=40, string="{}"),
                                        ],
                                    ),
                                    options=None,
                                ),
                            ],
                        ),
                        options=None,
                    ),
                ],
            ),
        ),
        pytest.param(
            r'@hello{} @hello[]{} @hello[x]{} @hello[x,]{}',
            FragmentList(
                start_pos=0, end_pos=44,
                children=[
                    PaxterFunc(
                        start_pos=0, end_pos=8,
                        id=Identifier(start_pos=1, end_pos=6, name="hello"),
                        fragments=FragmentList(start_pos=7, end_pos=7, children=[]),
                        options=None,
                    ),
                    Text(start_pos=8, end_pos=9, string=" "),
                    PaxterFunc(
                        start_pos=9, end_pos=19,
                        id=Identifier(start_pos=10, end_pos=15, name="hello"),
                        fragments=FragmentList(start_pos=18, end_pos=18, children=[]),
                        options=[],
                    ),
                    Text(start_pos=19, end_pos=20, string=" "),
                    PaxterFunc(
                        start_pos=20, end_pos=31,
                        id=Identifier(start_pos=21, end_pos=26, name="hello"),
                        fragments=FragmentList(start_pos=30, end_pos=30, children=[]),
                        options=[
                            (Identifier(start_pos=27, end_pos=28, name="x"), None),
                        ],
                    ),
                    Text(start_pos=31, end_pos=32, string=" "),
                    PaxterFunc(
                        start_pos=32, end_pos=44,
                        id=Identifier(start_pos=33, end_pos=38, name="hello"),
                        fragments=FragmentList(start_pos=43, end_pos=43, children=[]),
                        options=[
                            (Identifier(start_pos=39, end_pos=40, name="x"), None),
                        ],
                    ),
                ],
            ),
        ),
    ],
)
def test_parser(input_text, expected):
    parser = Parser()
    assert parser.parse(input_text) == expected
