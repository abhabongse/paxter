import pytest

from paxter.core.exceptions import PaxterConfigError, PaxterSyntaxError
from paxter.core.lexers import Lexer
from paxter.core.parser import Parser


@pytest.mark.parametrize(
    "switch",
    ["", "@%", "#", "{", "a", "ก"],
)
def test_invalid_switch(switch):
    with pytest.raises(PaxterConfigError):
        Lexer(switch=switch)


@pytest.mark.parametrize(
    ("input_text", "message_pattern"),
    [
        pytest.param(
            """\
                @hello<{{ }}>
                @hi##<#<{}>#>#
            """,
            r'cannot match closing pattern .* to the opening pattern .* '
            r'at line 2 col 26',
        ),
        pytest.param(
            """\
                @hello<{{ }}>
                @hi{  @#<{}>  }
            """,
            r'cannot match closing pattern .* to the opening pattern .* '
            r'at line 2 col 27',
        ),
        pytest.param(
            """\
                @hello<{{ }}>
                @-
            """,
            r'invalid expression after symbol .@. at line 2 col 17',
        ),
        pytest.param(
            """\
                @hello<{{ }}>
                @hi!##<#< {} >#>##
            """,
            r'expected opening brace after options at line 2 col 21',
        ),
        pytest.param(
            """\
                @hello<{{ }}>
                @hi[]##<#< {} >#>##
            """,
            r'expected opening brace after options at line 2 col 22',
        ),
        pytest.param(
            """\
                @hello<{{ }}>
                @hi[x,+]{}
            """,
            r'expected next option or a closing bracket at line 2 col 23',
        ),
        pytest.param(
            """\
                @hello<{{ }}>
                @hi[x+]{}
            """,
            r'expected a comma or a closing bracket at line 2 col 22',
        ),
    ],
)
def test_cannot_match_right_pattern_error(input_text, message_pattern):
    parser = Parser()
    with pytest.raises(PaxterSyntaxError, match=message_pattern):
        parser.parse(input_text)
