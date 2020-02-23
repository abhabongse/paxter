from paxter.parser import Paxter
from paxter.transformer import Transformer


def test_base_transformer():
    transformer = Transformer()

    input_text = """
        @bold{Tom @italic{and} Jerry}!
        My name is @name. I am @age years old!
        @!{italic("YAS")}
        @bold#<{##<#{}#>##}>#
    """

    expected_text = """
        <b>Tom <i>and</i> Jerry</b>!
        My name is John. I am 25 years old!
        <i>YAS</i>
        <b>##<#{}#>##</b>
    """

    environ = {
        # Macros
        '!': lambda env, token: eval(token, env),
        # Functions
        'bold': lambda token: f"<b>{token}</b>",
        'italic': lambda token: f"<i>{token}</i>",
        # Constants
        'name': "John",
        'age': 25,
    }

    parsed_tree = Paxter.parse(input_text)
    output_text = transformer.visit(environ, parsed_tree)
    assert output_text == expected_text
