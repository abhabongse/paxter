import pytest

from paxter.data import AtExpression, Fragments, Identifier, RawString
from paxter.parser import Paxter


@pytest.mark.parametrize(
    ("content", "expected"),
    [
        pytest.param(
            " @hello{ @hi{x} }>",
            Fragments(
                start=0, end=18,
                children=[
                    RawString(start=0, end=1, string=' '),
                    AtExpression(
                        start=1, end=17,
                        identifier=Identifier(start=2, end=7, name='hello'),
                        fragments=Fragments(
                            start=8, end=16,
                            children=[
                                RawString(start=8, end=9, string=' '),
                                AtExpression(
                                    start=9, end=15,
                                    identifier=Identifier(start=10, end=12,
                                                          name='hi'),
                                    fragments=Fragments(
                                        start=13, end=14,
                                        children=[
                                            RawString(start=13, end=14,
                                                      string='x'),
                                        ],
                                    ),
                                ),
                                RawString(start=15, end=16, string=' '),
                            ],
                        ),
                    ),
                    RawString(start=17, end=18, string='>')
                ],
            ),
        ),
        pytest.param(
            " @hello<{{}}>",
            Fragments(
                start=0, end=13,
                children=[
                    RawString(start=0, end=1, string=' '),
                    AtExpression(
                        start=1, end=13,
                        identifier=Identifier(start=2, end=7, name='hello'),
                        fragments=Fragments(
                            start=9, end=11,
                            children=[
                                RawString(start=9, end=11, string='{}'),
                            ],
                        ),
                    ),
                ],
            ),
        ),
        pytest.param(
            " @|he|llo @hello{} ",
            Fragments(
                start=0, end=19,
                children=[
                    RawString(start=0, end=1, string=" "),
                    AtExpression(
                        start=1, end=6,
                        identifier=Identifier(start=3, end=5, name="he"),
                        options={},
                        fragments=None,
                    ),
                    RawString(start=6, end=10, string="llo "),
                    AtExpression(
                        start=10, end=18,
                        identifier=Identifier(start=11, end=16, name="hello"),
                        options={},
                        fragments=Fragments(start=17, end=17, children=[]),
                    ),
                    RawString(start=18, end=19, string=" "),
                ],
            ),
        ),
    ],
)
def test_parser(content, expected):
    assert Paxter.parse(content) == expected

# TODO: add more unit tests for syntax errors
