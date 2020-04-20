import pytest  # noqa

from paxter.core import (
    FragmentList, Identifier, Number, Operator, Parser, PaxterApply, PaxterPhrase, Text,
    TokenList,
)


@pytest.mark.parametrize(
    ("input_text", "expected"),
    [
        pytest.param(
            "",
            FragmentList(children=[]),
        ),
        pytest.param(
            "1",
            FragmentList(children=[Text(inner='1')]),
        ),
        pytest.param(
            "@hello",
            FragmentList(children=[PaxterPhrase(inner='hello')]),
        ),
        pytest.param(
            "Hello, my name is @name.",
            FragmentList(
                children=[
                    Text(inner="Hello, my name is "),
                    PaxterPhrase(inner="name"),
                    Text(inner="."),
                ],
            ),
        ),
        pytest.param(
            "The result of 1 + 1 is @|1 + 1|. Yes! @<#|1 + 1|#>",
            FragmentList(
                children=[
                    Text(inner="The result of 1 + 1 is "),
                    PaxterPhrase(inner="1 + 1"),
                    Text(inner=". Yes! "),
                    PaxterPhrase(inner="1 + 1"),
                ],
            ),
        ),
        pytest.param(
            "@|N @ M @ K|",
            FragmentList(children=[PaxterPhrase(inner='N @ M @ K')]),
        ),
        pytest.param(
            "@<#|#|#|#>, @<<|<|>|>>, @@@,@;",
            FragmentList(
                children=[
                    PaxterPhrase(inner="#|#"),
                    Text(inner=", "),
                    PaxterPhrase(inner="<|>"),
                    Text(inner=", "),
                    PaxterPhrase(inner="@"),
                    PaxterPhrase(inner=","),
                    PaxterPhrase(inner=";"),
                ],
            ),
        ),
        pytest.param(
            "This is @em{not} a drill!",
            FragmentList(
                children=[
                    Text(inner="This is "),
                    PaxterApply(
                        id=Identifier(name="em"),
                        options=None,
                        main_arg=FragmentList(children=[Text(inner="not")]),
                    ),
                    Text(inner=" a drill!"),
                ],
            ),
        ),
        pytest.param(
            "Level 0 @level1{ @level2{ @level3 } }",
            FragmentList(
                children=[
                    Text(inner="Level 0 "),
                    PaxterApply(
                        id=Identifier(name="level1"),
                        options=None,
                        main_arg=FragmentList(
                            children=[
                                Text(inner=" "),
                                PaxterApply(
                                    id=Identifier(name="level2"),
                                    options=None,
                                    main_arg=FragmentList(
                                        children=[
                                            Text(inner=" "),
                                            PaxterPhrase(inner="level3"),
                                            Text(inner=" "),
                                        ],
                                    ),
                                ),
                                Text(inner=" "),
                            ],
                        ),
                    ),
                ],
            ),
        ),
        pytest.param(
            '@say[greet=@"hello"]{John} at @email<#"john@example.com"#>!',
            FragmentList(
                children=[
                    PaxterApply(
                        id=Identifier(name="say"),
                        options=TokenList(
                            children=[
                                Identifier(name="greet"),
                                Operator(symbol="="),
                                Text(inner="hello"),
                            ],
                        ),
                        main_arg=FragmentList(children=[Text(inner="John")]),
                    ),
                    Text(inner=" at "),
                    PaxterApply(
                        id=Identifier(name="email"),
                        options=None,
                        main_arg=Text(inner="john@example.com"),
                    ),
                    Text(inner="!"),
                ],
            ),
        ),
        pytest.param(
            '@state[x=1,y=2,z=3]#"This symbol " is a quote!"#',
            FragmentList(
                children=[
                    PaxterApply(
                        id=Identifier(name="state"),
                        options=TokenList(
                            children=[
                                Identifier(name="x"),
                                Operator(symbol="="),
                                Number(number=1),
                                Operator(symbol=","),
                                Identifier(name="y"),
                                Operator(symbol="="),
                                Number(number=2),
                                Operator(symbol=","),
                                Identifier(name="z"),
                                Operator(symbol="="),
                                Number(number=3),
                            ],
                        ),
                        main_arg=Text(inner='This symbol " is a quote!'),
                    ),
                ],
            ),
        ),
        pytest.param(
            '@"@a @|1 + 1|", @|@name{} @"John"|, @say"cheese not @name"',
            FragmentList(
                children=[
                    Text(inner="@a @|1 + 1|"),
                    Text(inner=", "),
                    PaxterPhrase(inner='@name{} @"John"'),
                    Text(inner=", "),
                    PaxterApply(
                        id=Identifier(name="say"),
                        options=None,
                        main_arg=Text(inner="cheese not @name"),
                    ),
                ],
            ),
        ),
        pytest.param(
            '@|| @{} @"" @#||# @<{}> @<#""#>',
            FragmentList(
                children=[
                    PaxterPhrase(inner=""),
                    Text(inner=" "),
                    FragmentList(children=[]),
                    Text(inner=" "),
                    Text(inner=""),
                    Text(inner=" "),
                    PaxterPhrase(inner=""),
                    Text(inner=" "),
                    FragmentList(children=[]),
                    Text(inner=" "),
                    Text(inner=""),
                ],
            ),
        ),
        pytest.param(
            '@foo[bar = @"x" + @foo[bar=@{x}|>3]]',
            FragmentList(
                children=[
                    PaxterApply(
                        id=Identifier(name="foo"),
                        options=TokenList(
                            children=[
                                Identifier(name="bar"),
                                Operator(symbol="="),
                                Text(inner="x"),
                                Operator(symbol="+"),
                                PaxterApply(
                                    id=Identifier(name="foo"),
                                    options=TokenList(
                                        children=[
                                            Identifier(name="bar"),
                                            Operator(symbol="="),
                                            FragmentList(children=[Text(inner="x")]),
                                            Operator(symbol="|>"),
                                            Number(number=3),
                                        ],
                                    ),
                                    main_arg=None,
                                ),
                            ],
                        ),
                        main_arg=None,
                    ),
                ],
            ),
        ),
        pytest.param(
            '@{@{@expand[1->2,<-3,stop,@"foo",,@cool]{@|4+4|}}}',
            FragmentList(
                children=[
                    FragmentList(
                        children=[
                            FragmentList(
                                children=[
                                    PaxterApply(
                                        id=Identifier(name="expand"),
                                        options=TokenList(
                                            children=[
                                                Number(number=1),
                                                Operator(symbol="->"),
                                                Number(number=2),
                                                Operator(symbol=","),
                                                Operator(symbol="<-"),
                                                Number(number=3),
                                                Operator(symbol=","),
                                                Identifier(name="stop"),
                                                Operator(symbol=","),
                                                Text(inner="foo"),
                                                Operator(symbol=","),
                                                Operator(symbol=","),
                                                PaxterPhrase(inner="cool"),
                                            ],
                                        ),
                                        main_arg=FragmentList(
                                            children=[PaxterPhrase(inner="4+4")],
                                        ),
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
        ),
        pytest.param(
            "@foo[()->(),{}->[]]",
            FragmentList(
                children=[
                    PaxterApply(
                        id=Identifier(name="foo"),
                        options=TokenList(
                            children=[
                                TokenList(children=[]),
                                Operator(symbol="->"),
                                TokenList(children=[]),
                                Operator(symbol=","),
                                TokenList(children=[]),
                                Operator(symbol="->"),
                                TokenList(children=[]),
                            ],
                        ),
                        main_arg=None,
                    ),
                ],
            ),
        ),
    ],
)
def test_parser(input_text, expected):
    assert Parser.parse(input_text) == expected

# TODO: need to add a lot more unit tests
