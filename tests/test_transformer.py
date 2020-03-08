import pytest

from paxter.core import Parser
from paxter.standard import SimplePythonTransformer

fst_environment = {
    'name': "John",
    'age': 25,
    'bold': lambda token: f"<b>{token}</b>",
    'italic': lambda token: f"<i>{token}</i>",
    'tag': lambda token, tag: f"<{tag}>{token}</{tag}>",
}
fst_input_text = """\
john@"@"example.com
@<#"sarah@example.com"#>
@bold{Tom @italic{and} Jerry}!
@{italic("YAS")}
@bold#<{##<#{}#>##}>#
@tag[tag="u"]{works fine!}

My name is @name. I am @age years old!
@!{age = age + 1}
My name is @name. I am @age years old!
"""
fst_expected = """\
john@example.com
sarah@example.com
<b>Tom <i>and</i> Jerry</b>!
<i>YAS</i>
<b>##<#{}#>##</b>
<u>works fine!</u>

My name is John. I am 25 years old!

My name is John. I am 26 years old!
"""

snd_environment = {}
snd_input_text = """\
@!{
x = 1
def add(_, a, b):
    return a + b
}
@x and @add[a=x,b=2]{}
"""
snd_expected = """\

1 and 3
"""

trd_environment = {
    'name': "John Smith",
    'age_last_year': 47,
    'strip': lambda token: token.strip(),
    'tag': lambda token, label: f"<{label}>{token}</{label}>",
}
trd_input_text = '''\
@!##{
def add_one(num):
    return num + 1
}##

Hello, my @strip{  full name   } is @name.
@tag[label="b"]{@name is @{age_last_year + 1} years old.}
@!{age_this_year = age_last_year + 1}

Do you know that 1 + 1 = @{1 + 1}?
'''
trd_expected = '''\


Hello, my full name is John Smith.
<b>John Smith is 48 years old.</b>


Do you know that 1 + 1 = 2?
'''


@pytest.mark.parametrize(
    ("environment", "input_text", "expected"),
    [
        (fst_environment, fst_input_text, fst_expected),
        (snd_environment, snd_input_text, snd_expected),
        (trd_environment, trd_input_text, trd_expected),
    ],
)
def test_simple_python_transformer(environment, input_text, expected):
    parser = Parser()
    transformer = SimplePythonTransformer()
    parsed_tree = parser.parse(input_text)
    _, output_text = transformer.transform(environment, parsed_tree)
    assert output_text == expected


def test_environment_change():
    parser = Parser()
    transformer = SimplePythonTransformer()

    parsed_tree = parser.parse(fst_input_text)
    updated_environment, _ = transformer.transform(fst_environment, parsed_tree)
    assert updated_environment['age'] == 26

    parsed_tree = parser.parse(trd_input_text)
    updated_environment, _ = transformer.transform(trd_environment, parsed_tree)
    assert updated_environment['age_this_year'] == 48
