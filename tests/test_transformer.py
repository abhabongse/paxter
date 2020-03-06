import pytest

from paxter.core import Parser, SimplePythonTransformer


@pytest.mark.parametrize(
    ("input_text", "expected", "final_age"),
    [
        ("""\
john@"@"example.com
@<#"sarah@example.com"#>
@bold{Tom @italic{and} Jerry}!
@{italic("YAS")}
@bold#<{##<#{}#>##}>#
@tag[tag="u"]{works fine!}

My name is @name. I am @age years old!
@!{age = age + 1}
My name is @name. I am @age years old!
""", """\
john@example.com
sarah@example.com
<b>Tom <i>and</i> Jerry</b>!
<i>YAS</i>
<b>##<#{}#>##</b>
<u>works fine!</u>

My name is John. I am 25 years old!

My name is John. I am 26 years old!
""", 26),
        ("""\
@!{
x = 1
def add(_, a, b):
    return a + b
}
@x and @add[a=x,b=2]{}
""", """\

1 and 3
""",  25),
    ],
)
def test_bottom_up_transformer(input_text, expected, final_age):
    parser = Parser()
    transformer = SimplePythonTransformer()
    environ = {
        # Functions
        'bold': lambda token: f"<b>{token}</b>",
        'italic': lambda token: f"<i>{token}</i>",
        'tag': lambda token, tag: f"<{tag}>{token}</{tag}>",
        # Constants
        'name': "John",
        'age': 25,
    }

    parsed_tree = parser.parse(input_text)
    final_environ, output_text = transformer.transform(environ, parsed_tree)
    assert output_text == expected
    assert final_environ['age'] == final_age
