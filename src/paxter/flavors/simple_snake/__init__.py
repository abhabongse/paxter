"""
**Simple Snake** is the name of one possible flavor of interpretation
of parsed trees under Paxter language.
It allows python code to be embedded within the input document text itself.

## Interpretation of Parsed Tree

### Node Transformation

- Each `paxter.core.data.PaxterPhrase` evaluates its main text as python expression.
  Result of the evaluation will be output to the transformed text.

- Each `paxter.core.data.PaxterFunc` will be a function application
  of a function (which is indicated by its identifier part)
  with the main text part as the only positional argument.
  Specified options will be passed to the same function call as keyword arguments.

- Each `paxter.core.data.PaxterMacro` will be a function application
  of a function (which is indicated by its identifier ending with a `!`)
  with two positional arguments: the environment dict and the main text respectively.

### Execution Environment

For each tree transformation, a fresh copy of environment dict will be created
using the following data in this order
(the repeated appearance of a key will override previous values).

1.  [`__builtins__`](https://docs.python.org/3/library/functions.html)
    will be introduced automatically.

2.  JSON literal constants: `null`, `true`, and `false`
    for `None`, `True`, and `False` python values respectively.

3.  These following macros:

    - The single `!` macro which simply executes the main text input as python code.
      To print to the output text at the same location,
      the code must write to the `StringIO` object called `buffer`
      which will be temporarily be injected into each `!` macro call.
      [See examples below.](#buffer-example)

    - The `load!` macro which loads a set of extra functions into the environment.
      Available sets are `string`, `html`, and `base64`.
      See more at `paxter.flavors.simple_snake.functions`.

4.  Starting environment dict `start_env` provided at the construction
    of the `paxter.flavors.simple_snake.SimpleSnakeTransformer` instance.

5.  Environment dict provided to the
    `paxter.flavors.simple_snake.SimpleSnakeTransformer.transform` method.

6.  Any side-effects happen during the interpretation of the input text.

### Post Processing

At the end of the transformation, if a line ends with a backslash,
then the backslash itself along with the newline character next to it
will be removed from the output text.

## Example

### Buffer Example


"""
from paxter.core.transformer import visitor_method_names
from paxter.flavors.simple_snake._transformer import SimpleSnakeTransformer

__all__ = ['SimpleSnakeTransformer']

__pdoc__ = {
    f'SimpleSnakeTransformer.{attrib}': False
    for attrib in visitor_method_names
}
