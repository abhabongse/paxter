"""
**Simple Snake** is the name of one possible flavor of interpretation
of parsed trees under Paxter language.
It allows python code to be embedded within the input document text itself.

## Interpretation of Parsed Tree

### Node Transformation

-   Each `paxter.core.data.PaxterPhrase` evaluates its main text as python expression.
    Result of the evaluation will be output to the transformed text.

-   Each `paxter.core.data.PaxterFunc` will be a function application
    of a function (which is indicated by its identifier part)
    with the main text part as the only positional argument.
    Specified options will be passed to the same function call as keyword arguments.

-   Each `paxter.core.data.PaxterMacro` will be a function application
    of a function (which is indicated by its identifier ending with a `!`)
    with two positional arguments: the environment dict and the main text respectively.

### Execution Environment

For each tree transformation, a fresh copy of environment dict will be created
using the following data in this order
(the repeated appearance of a key will override previous values).

1.  [`__builtins__`](https://docs.python.org/3/library/functions.html)
    will be introduced automatically.

2.  Pre-defined identifiers: `true`, `false`, `null`,
    single `!` macro, `load!` macro, and `if` and `for` statement patterns.
    [More details below.](#special-patterns)

3.  Starting environment dict `start_env` provided at the construction
    of the `paxter.flavors.simple_snake.SimpleSnakeTransformer` instance.

4.  Environment dict provided to the
    `paxter.flavors.simple_snake.SimpleSnakeTransformer.transform` method.

5.  Any side-effects happen during the interpretation of the input text.

### Pre-defined Identifiers

-   Identifiers `true`, `false`, and `null` correspond to
    JSON literals of the same which.
    Their python counterparts are `True`, `False`, and `None` respectively.

-   The single `!` macro simply executes the main text input as python code.

    To print to the output space at the same location the macro appear in,
    the python code must write to the `StringIO` object called `buffer`
    which will temporarily be injected into the environment of each macro call.
    For example,

        @!##{
            print("Hello, World!", file=buffer)
        }##

-   The `load!` macro which loads a set of extra definitions
    (values and functions) into the environment.
    Available sets are `string`, `html`, and `base64`.

-   Paxter function expression of the form `@if[<test>,<bool>]{...}`
    is a special if-statement pattern in Simple Snake.

    The `<bool>` part must either be exactly the literal `true` or `false`.
    If this part is absent as in `@if[<test>]{...}`, then `true` will be assumed.

    The `<test>` part must be an identifier which will be tested for truthiness.
    If it is a callable, then it will be invoked first without arguments.

    When the `<test>` part is evaluated for truthiness,
    its result with be compared with `<bool>` part.
    Then the main text will be evaluated if and only if the comparison matches.

-   Paxter function expression of the form `@for[<item_id>,<seq>]{...}`
    is a special for-statement pattern in Simple Snake.

    The identifier presented at the `<item_id>` part will bind to
    each item produced by the identifier at the `<seq>` part,
    which will appear in the environment while evaluating the main text.

    The main text will be repeatedly evaluated for each item in `<seq>`,
    and the final result will be the concatenation of the evaluated result
    of the main text from each loop iteration.

### Post Processing

At the end of the transformation, if a line ends with a backslash,
then the backslash itself along with the newline character next to it
will be removed from the output text.
"""
from paxter.core.transformer import visitor_method_names
from paxter.flavors.simple_snake._transformer import SimpleSnakeTransformer
from paxter.flavors.simple_snake._utils import DefinitionSet, with_env, with_node

__all__ = ['SimpleSnakeTransformer', 'DefinitionSet', 'with_env', 'with_node']

__pdoc__ = {
    f'SimpleSnakeTransformer.{attrib}': False
    for attrib in visitor_method_names
}
