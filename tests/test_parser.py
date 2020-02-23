import pytest

from paxter.data import AtExprFunc, AtExprMacro, Fragments, Identifier, RawText
from paxter.parser import Paxter


@pytest.mark.parametrize(
    ("input_text", "expected"),
    [
        pytest.param(
            " @hello{ @hi{x} }>",
            Fragments(
                start=0, end=18,
                children=[
                    RawText(start=0, end=1, string=" "),
                    AtExprFunc(
                        start=1, end=17,
                        identifier=Identifier(start=2, end=7, name="hello"),
                        fragments=Fragments(
                            start=8, end=16,
                            children=[
                                RawText(start=8, end=9, string=" "),
                                AtExprFunc(
                                    start=9, end=15,
                                    identifier=Identifier(start=10, end=12, name="hi"),
                                    fragments=Fragments(
                                        start=13, end=14,
                                        children=[
                                            RawText(start=13, end=14, string="x")
                                        ],
                                    ),
                                    options={},
                                ),
                                RawText(start=15, end=16, string=" "),
                            ],
                        ),
                        options={},
                    ),
                    RawText(start=17, end=18, string=">"),
                ],
            ),
        ),
        pytest.param(
            " @hello<{{}}>",
            Fragments(
                start=0, end=13,
                children=[
                    RawText(start=0, end=1, string=" "),
                    AtExprFunc(
                        start=1, end=13,
                        identifier=Identifier(start=2, end=7, name="hello"),
                        fragments=Fragments(
                            start=9, end=11,
                            children=[RawText(start=9, end=11, string="{}")]
                        ),
                        options={},
                    ),
                ],
            ),
        ),
        pytest.param(
            " @hey!{@>@} ",
            Fragments(
                start=0, end=12,
                children=[
                    RawText(start=0, end=1, string=" "),
                    AtExprMacro(
                        start=1, end=11,
                        identifier=Identifier(start=2, end=5, name="hey"),
                        raw_text=RawText(start=7, end=10, string="@>@"),
                    ),
                    RawText(start=11, end=12, string=" "),
                ],
            ),
        ),
        pytest.param(
            "@!{@hello{}}",
            Fragments(
                start=0, end=12,
                children=[
                    AtExprMacro(
                        start=0, end=11,
                        identifier=Identifier(start=1, end=1, name=""),
                        raw_text=RawText(start=3, end=10, string="@hello{"),
                    ),
                    RawText(start=11, end=12, string="}"),
                ],
            ),
        ),
        pytest.param(
            "@!#{@hello{}}#",
            Fragments(
                start=0, end=14,
                children=[
                    AtExprMacro(
                        start=0, end=14,
                        identifier=Identifier(start=1, end=1, name=""),
                        raw_text=RawText(start=4, end=12, string="@hello{}"),
                    )
                ],
            ),
        ),
        pytest.param(
            "@hello{@hi}",
            Fragments(
                start=0, end=11,
                children=[
                    AtExprFunc(
                        start=0, end=11,
                        identifier=Identifier(start=1, end=6, name="hello"),
                        fragments=Fragments(
                            start=7, end=10,
                            children=[
                                AtExprMacro(
                                    start=7, end=10,
                                    identifier=Identifier(start=8, end=8, name=""),
                                    raw_text=RawText(start=8, end=10, string="hi"),
                                )
                            ],
                        ),
                        options={},
                    )
                ],
            ),
        ),
    ],
)
def test_parser(input_text, expected):
    assert Paxter.parse(input_text) == expected

# TODO: add more unit tests for syntax errors
