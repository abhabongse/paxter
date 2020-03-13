import pytest

from paxter.core.data import PaxterFunc
from paxter.core.exceptions import PaxterTransformError
from paxter.core.parser import Parser


@pytest.mark.parametrize(
    ("input_text", "expected"),
    [
        ('@hello[]{}', ()),
        ('@hello["x"]{}', ()),
        ('@hello[hi,"x",yes]{}', {0: 'hi', 2: 'yes'}),
        ('@hello[r]{}', {0: 'r'}),
        ('@hello[a,b,c]{}', {0: 'a', 1: 'b', 2: 'c'}),
        ('@hello[a=1,b=2,c=3,x,y,z]{}', {3: 'x', 4: 'y', 5: 'z'}),
        ('@hello["k",2,g,n=2]{}', {2: 'g'}),
    ],
)
def test_faux_key(input_text, expected):
    parser = Parser()
    tree = parser.parse(input_text)
    node = tree.children[0]
    assert isinstance(node, PaxterFunc)

    for index, kv_pair in enumerate(node.options):
        if index in expected:
            assert kv_pair.get_faux_key() == expected[index]
        else:
            with pytest.raises(PaxterTransformError):
                kv_pair.get_faux_key()
