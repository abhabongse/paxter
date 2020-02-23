from paxter.parser import Paxter
from paxter.transformer import Transformer

transformer = Transformer()

INPUT_TEXT = """
    @bold{Tom @italic{and} Jerry}!
    My name is @name. I am @age years old!
    @!{italic("YAS")}
    @bold#<{##<#{}#>##}>#
"""

EXPECTED_TEXT = """
    <b>Tom <i>and</i> Jerry</b>!
    My name is John. I am 25 years old!
    <i>YAS</i>
    <b>##<#{}#>##</b>
"""

ENV = {
    '__builtins__': {},
    'bold': lambda token: f"<b>{token}</b>",
    'italic': lambda token: f"<i>{token}</i>",
    '!': lambda env, token: eval(token, env),
    'name': "John",
    'age': 25,
}


def test_base_transformer():
    parsed_tree = Paxter.parse(INPUT_TEXT)
    output_text = transformer.visit(ENV, parsed_tree)
    assert output_text == EXPECTED_TEXT
