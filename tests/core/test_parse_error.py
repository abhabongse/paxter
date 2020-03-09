import pytest

from paxter.core.exceptions import PaxterSyntaxError
from paxter.core.parser import Parser


def test_cannot_match_right_pattern_error():
    parser = Parser()
    input_text = """\
@hello<{{ }}>
@hi{  @#<{}>  }
"""
    with pytest.raises(
            PaxterSyntaxError,
            match=r'cannot match closing pattern .* '
                  r'to the opening pattern .* '
                  r'at line 2 col 11',
    ):
        parser.parse(input_text)
