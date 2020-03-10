from paxter.core import Parser
from paxter.flavors import SimpleSnakeTransformer


def test_functions():
    parser = Parser()
    transformer = SimpleSnakeTransformer()

    input_text = """\
@load!{string}@load!{html}@load!{base64}\
@capitalize{hello world}
@casefold{schweiß}
|@centering[width=11,fillchar="_"]{beans}|
@expandtabs{x}
|@rjust[width=6]{yes}@ljust[width=5]{no}|
@to_lower{LOWER}@to_upper{upper}
@rstrip{Left   } and @lstrip{    Right}
@replace[old="a",new="b",count=2]{asdfasdfasdf}
|@strip{  answer  }|
@swapcase{asdf@swapcase{ςσ}}
@maketitle{one two three}
@zfill[width=5]{-4}

@html_escape{<a>}
@html_unescape{&lt;a&gt;}
@standard_b64encode{éçก}
@standard_b64decode{w6nDp+C4gQ==}
@urlsafe_b64encode{éçก}
@urlsafe_b64decode{w6nDp-C4gQ==}

@indent[prefix="_"]<{
one

two
}>\
@dedent{
    one

    two
        three
}
@linewrap[width=8]{abc def gh ij kl mn}
@truncate_word[width=10]{abc defg hij}
@truncate[width=10]{abc defg hij}
"""
    expected = """\
Hello world
schweiss
|___beans___|
x
|   yesno   |
lowerUPPER
Left and Right
bsdfbsdfasdf
|answer|
ASDFσς
One Two Three
-0004

&lt;a&gt;
<a>
w6nDp+C4gQ==
éçก
w6nDp-C4gQ==
éçก


_one

_two
one

two
    three
abc def
gh ij kl
mn
abc...
abc def...
"""
    tree = parser.parse(input_text)
    _, output_text = transformer.transform({}, tree)
    assert output_text == expected
