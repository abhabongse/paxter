import pytest

from paxter.data import AtNormalExpr, Fragments, Identifier, RawString
from paxter.parser import Paxter


@pytest.mark.parametrize(
    ("content", "expected"),
    [
        (" @hello{ @hi{x} }>",
         Fragments(
             start=0, end=18,
             nodes=[
                 RawString(start=0, end=1, text=' '),
                 AtNormalExpr(
                     start=1, end=17,
                     identifier=Identifier(start=2, end=7, name='hello'),
                     fragments=Fragments(
                         start=8, end=16,
                         nodes=[
                             RawString(start=8, end=9, text=' '),
                             AtNormalExpr(
                                 start=9, end=15,
                                 identifier=Identifier(start=10, end=12, name='hi'),
                                 fragments=Fragments(
                                     start=13, end=14,
                                     nodes=[
                                         RawString(start=13, end=14, text='x'),
                                     ],
                                 ),
                             ),
                             RawString(start=15, end=16, text=' '),
                         ],
                     ),
                 ),
                 RawString(start=17, end=18, text='>')
             ],
         )),
        (" @hello<{{}}>",
         Fragments(
             start=0, end=13,
             nodes=[
                 RawString(start=0, end=1, text=' '),
                 AtNormalExpr(
                     start=1, end=13,
                     identifier=Identifier(start=2, end=7, name='hello'),
                     fragments=Fragments(
                         start=9, end=11,
                         nodes=[
                             RawString(start=9, end=11, text='{}'),
                         ],
                     ),
                 ),
             ],
         )),
    ],
    # TODO: add more tests for macro @-expr
)
def test_parser(content, expected):
    assert Paxter.parse(content) == expected
