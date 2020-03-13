import pytest

from paxter.core import (FragmentList, Identifier, KeyValue, Literal, Parser,
                         PaxterFunc, PaxterMacro, PaxterPhrase, Text)


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
                        options=None,
                        fragments=FragmentList(
                            start_pos=8, end_pos=16,
                            children=[
                                Text(start_pos=8, end_pos=9, string=" "),
                                PaxterFunc(
                                    start_pos=9, end_pos=15,
                                    id=Identifier(start_pos=10, end_pos=12, name="hi"),
                                    options=None,
                                    fragments=FragmentList(
                                        start_pos=13, end_pos=14,
                                        children=[
                                            Text(start_pos=13, end_pos=14, string="x"),
                                        ],
                                    ),
                                ),
                                Text(start_pos=15, end_pos=16, string=" "),
                            ],
                        ),
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
                        options=None,
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
                                    options=None,
                                    fragments=FragmentList(
                                        start_pos=17, end_pos=18,
                                        children=[
                                            Text(start_pos=17, end_pos=18, string="1"),
                                        ],
                                    ),
                                ),
                                Text(start_pos=19, end_pos=20, string="_"),
                            ],
                        ),
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
                        options=None,
                        fragments=FragmentList(
                            start_pos=9, end_pos=11,
                            children=[Text(start_pos=9, end_pos=11, string="{}")],
                        ),
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
                        options=None,
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
                        options=None,
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
                        options=None,
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
                        options=None,
                        fragments=FragmentList(
                            start_pos=7, end_pos=10,
                            children=[
                                PaxterPhrase(
                                    start_pos=7, end_pos=10,
                                    phrase=Text(start_pos=8, end_pos=10, string="hi"),
                                ),
                            ],
                        ),
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
                        options=None,
                        fragments=FragmentList(
                            start_pos=7, end_pos=42,
                            children=[
                                PaxterFunc(
                                    start_pos=7, end_pos=42,
                                    id=Identifier(
                                        start_pos=8, end_pos=13,
                                        name="hello",
                                    ),
                                    options=None,
                                    fragments=FragmentList(
                                        start_pos=15, end_pos=40,
                                        children=[
                                            PaxterFunc(
                                                start_pos=15, end_pos=38,
                                                id=Identifier(
                                                    start_pos=16, end_pos=21,
                                                    name="hello",
                                                ),
                                                options=None,
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
                                            ),
                                            Text(start_pos=38, end_pos=40, string="{}"),
                                        ],
                                    ),
                                ),
                            ],
                        ),
                    ),
                ],
            ),
        ),
        pytest.param(
            r'@hello{} @hello[]{} '
            r'@hello[x1]{} @hello[x2,]{} '
            r'@hello[3]{} @hello[4,]{} '
            r'@hello["5"]{} @hello["6",]{} '
            r'@hello[x7=x8]{} @hello[x9=x10,]{} '
            r'@hello[x11=12]{} @hello[x13=14,]{} '
            r'@hello[x15="16"]{} @hello[x17="18"]{}',
            FragmentList(
                start_pos=0, end_pos=207,
                children=[
                    PaxterFunc(
                        start_pos=0, end_pos=8,
                        id=Identifier(start_pos=1, end_pos=6, name="hello"),
                        options=None,
                        fragments=FragmentList(start_pos=7, end_pos=7, children=[]),
                    ),
                    Text(start_pos=8, end_pos=9, string=" "),
                    PaxterFunc(
                        start_pos=9, end_pos=19,
                        id=Identifier(start_pos=10, end_pos=15, name="hello"),
                        options=[],
                        fragments=FragmentList(start_pos=18, end_pos=18, children=[]),
                    ),
                    Text(start_pos=19, end_pos=20, string=" "),
                    PaxterFunc(
                        start_pos=20, end_pos=32,
                        id=Identifier(start_pos=21, end_pos=26, name="hello"),
                        options=[
                            KeyValue(
                                k=None,
                                v=Identifier(start_pos=27, end_pos=29, name="x1"),
                            ),
                        ],
                        fragments=FragmentList(start_pos=31, end_pos=31, children=[]),
                    ),
                    Text(start_pos=32, end_pos=33, string=" "),
                    PaxterFunc(
                        start_pos=33, end_pos=46,
                        id=Identifier(start_pos=34, end_pos=39, name="hello"),
                        options=[
                            KeyValue(
                                k=None,
                                v=Identifier(start_pos=40, end_pos=42, name="x2"),
                            ),
                        ],
                        fragments=FragmentList(start_pos=45, end_pos=45, children=[]),
                    ),
                    Text(start_pos=46, end_pos=47, string=" "),
                    PaxterFunc(
                        start_pos=47, end_pos=58,
                        id=Identifier(start_pos=48, end_pos=53, name="hello"),
                        options=[
                            KeyValue(
                                k=None,
                                v=Literal(start_pos=54, end_pos=55, value=3),
                            ),
                        ],
                        fragments=FragmentList(start_pos=57, end_pos=57, children=[]),
                    ),
                    Text(start_pos=58, end_pos=59, string=" "),
                    PaxterFunc(
                        start_pos=59, end_pos=71,
                        id=Identifier(start_pos=60, end_pos=65, name="hello"),
                        options=[
                            KeyValue(
                                k=None,
                                v=Literal(start_pos=66, end_pos=67, value=4),
                            ),
                        ],
                        fragments=FragmentList(start_pos=70, end_pos=70, children=[]),
                    ),
                    Text(start_pos=71, end_pos=72, string=" "),
                    PaxterFunc(
                        start_pos=72, end_pos=85,
                        id=Identifier(start_pos=73, end_pos=78, name="hello"),
                        options=[
                            KeyValue(
                                k=None,
                                v=Literal(start_pos=79, end_pos=82, value="5"),
                            ),
                        ],
                        fragments=FragmentList(start_pos=84, end_pos=84, children=[]),
                    ),
                    Text(start_pos=85, end_pos=86, string=" "),
                    PaxterFunc(
                        start_pos=86, end_pos=100,
                        id=Identifier(start_pos=87, end_pos=92, name="hello"),
                        options=[
                            KeyValue(
                                k=None,
                                v=Literal(start_pos=93, end_pos=96, value="6"),
                            ),
                        ],
                        fragments=FragmentList(start_pos=99, end_pos=99, children=[]),
                    ),
                    Text(start_pos=100, end_pos=101, string=" "),
                    PaxterFunc(
                        start_pos=101, end_pos=116,
                        id=Identifier(start_pos=102, end_pos=107, name="hello"),
                        options=[
                            KeyValue(
                                k=Identifier(start_pos=108, end_pos=110, name="x7"),
                                v=Identifier(start_pos=111, end_pos=113, name="x8"),
                            ),
                        ],
                        fragments=FragmentList(start_pos=115, end_pos=115, children=[]),
                    ),
                    Text(start_pos=116, end_pos=117, string=" "),
                    PaxterFunc(
                        start_pos=117, end_pos=134,
                        id=Identifier(start_pos=118, end_pos=123, name="hello"),
                        options=[
                            KeyValue(
                                k=Identifier(start_pos=124, end_pos=126, name="x9"),
                                v=Identifier(start_pos=127, end_pos=130, name="x10"),
                            ),
                        ],
                        fragments=FragmentList(start_pos=133, end_pos=133, children=[]),
                    ),
                    Text(start_pos=134, end_pos=135, string=" "),
                    PaxterFunc(
                        start_pos=135, end_pos=151,
                        id=Identifier(start_pos=136, end_pos=141, name="hello"),
                        options=[
                            KeyValue(
                                k=Identifier(start_pos=142, end_pos=145, name="x11"),
                                v=Literal(start_pos=146, end_pos=148, value=12),
                            ),
                        ],
                        fragments=FragmentList(start_pos=150, end_pos=150, children=[]),
                    ),
                    Text(start_pos=151, end_pos=152, string=" "),
                    PaxterFunc(
                        start_pos=152, end_pos=169,
                        id=Identifier(start_pos=153, end_pos=158, name="hello"),
                        options=[
                            KeyValue(
                                k=Identifier(start_pos=159, end_pos=162, name="x13"),
                                v=Literal(start_pos=163, end_pos=165, value=14),
                            ),
                        ],
                        fragments=FragmentList(start_pos=168, end_pos=168, children=[]),
                    ),
                    Text(start_pos=169, end_pos=170, string=" "),
                    PaxterFunc(
                        start_pos=170, end_pos=188,
                        id=Identifier(start_pos=171, end_pos=176, name="hello"),
                        options=[
                            KeyValue(
                                k=Identifier(start_pos=177, end_pos=180, name="x15"),
                                v=Literal(start_pos=181, end_pos=185, value="16"),
                            ),
                        ],
                        fragments=FragmentList(start_pos=187, end_pos=187, children=[]),
                    ),
                    Text(start_pos=188, end_pos=189, string=" "),
                    PaxterFunc(
                        start_pos=189, end_pos=207,
                        id=Identifier(start_pos=190, end_pos=195, name="hello"),
                        options=[
                            KeyValue(
                                k=Identifier(start_pos=196, end_pos=199, name="x17"),
                                v=Literal(start_pos=200, end_pos=204, value="18"),
                            ),
                        ],
                        fragments=FragmentList(start_pos=206, end_pos=206, children=[]),
                    ),
                ],
            ),
        ),
        pytest.param(
            r'@hello![x=100,y,z=a]{@hi{}}',
            FragmentList(
                start_pos=0, end_pos=27,
                children=[
                    PaxterMacro(
                        start_pos=0, end_pos=26,
                        id=Identifier(start_pos=1, end_pos=7, name="hello!"),
                        options=[
                            KeyValue(
                                k=Identifier(start_pos=8, end_pos=9, name="x"),
                                v=Literal(start_pos=10, end_pos=13, value=100),
                            ),
                            KeyValue(
                                k=None,
                                v=Identifier(start_pos=14, end_pos=15, name="y"),
                            ),
                            KeyValue(
                                k=Identifier(start_pos=16, end_pos=17, name="z"),
                                v=Identifier(start_pos=18, end_pos=19, name="a"),
                            ),
                        ],
                        text=Text(start_pos=21, end_pos=25, string="@hi{"),
                    ),
                    Text(start_pos=26, end_pos=27, string="}"),
                ],
            ),
        ),
    ],
)
def test_parser(input_text, expected):
    parser = Parser()
    assert parser.parse(input_text) == expected
