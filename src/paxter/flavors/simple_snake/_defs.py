"""
Definition sets to be available inside **Simple Snake** flavor.

## Pre-defined Definition Set

-   Definition Set `string`

    Available functions are `capitalize`, `casefold`, `centering`, `dedent`,
    `expandtabs`, `indent`, `linewrap`, `ljust`, `lstrip`, `maketitle`, `replace`,
    `rjust`, `rstrip`, `strip`, `swapcase`, `to_lower`, `to_upper`, `truncate`,
    `truncate_word`, and `zfill`.

-   Definition Set `html`

    Available functions are `html_escape` and `html_unescape`.

-   Definition Set `base64`

    Available functions are `standard_b64encode`, `standard_b64decode`,
    `urlsafe_b64encode`, and `urlsafe_b64decode`.
"""
import base64
import html
import inspect
import io
import textwrap
from typing import List, Optional, TYPE_CHECKING

from paxter.core import KeyValue, PaxterFunc, PaxterTransformError
from paxter.flavors.simple_snake._utils import DefinitionSet, with_env, with_node

if TYPE_CHECKING:
    from paxter.flavors.simple_snake._transformer import SimpleSnakeTransformer


#  ____  _        _
# / ___|| |_ _ __(_)_ __   __ _
# \___ \| __| '__| | '_ \ / _` |
#  ___) | |_| |  | | | | | (_| |
# |____/ \__|_|  |_|_| |_|\__, |
#                         |___/

string_set = DefinitionSet()


@string_set.register
def capitalize(text: str) -> str:
    """Alias for `str.capitalize`"""
    return text.capitalize()


@string_set.register
def casefold(text: str) -> str:
    """Alias for `str.casefold`"""
    return text.casefold()


@string_set.register
def centering(text: str, width: int, fillchar: str = ' ') -> str:
    """Alias for `str.center`"""
    return text.center(width, fillchar)


@string_set.register
def dedent(text: str) -> str:
    """Alias for `inspect.cleandoc`"""
    return inspect.cleandoc(text)


@string_set.register
def expandtabs(text: str, tabsize: int = 8) -> str:
    """Alias for `str.expandtabs`"""
    return text.expandtabs(tabsize)


@string_set.register
def indent(text: str, prefix: str) -> str:
    """Alias for `textwrap.indent`"""
    return textwrap.indent(text, prefix)


@string_set.register
def linewrap(text: str, width: int = 70) -> str:
    """Alias for `textwrap.fill`"""
    return textwrap.fill(text, width)


@string_set.register
def ljust(text: str, width: int, fillchar: str = ' ') -> str:
    """Alias for `str.ljust`"""
    return text.ljust(width, fillchar)


@string_set.register
def lstrip(text: str, chars: Optional[str] = None) -> str:
    """Alias for `str.lstrip`"""
    return text.lstrip(chars)


@string_set.register
def maketitle(text: str) -> str:
    """Alias for `str.title`"""
    return text.title()


@string_set.register
def replace(text: str, old: str, new: str, count: int = -1) -> str:
    """Alias for `str.replace`"""
    return text.replace(old, new, count)


@string_set.register
def rjust(text: str, width: int, fillchar: str = ' ') -> str:
    """Alias for `str.rjust`"""
    return text.rjust(width, fillchar)


@string_set.register
def rstrip(text: str, chars: Optional[str] = None) -> str:
    """Alias for `str.rstrip`"""
    return text.rstrip(chars)


@string_set.register
def strip(text: str, chars: Optional[str] = None) -> str:
    """Alias for `str.strip`"""
    return text.strip(chars)


@string_set.register
def swapcase(text: str) -> str:
    """Alias for `str.swapcase`"""
    return text.swapcase()


@string_set.register
def to_lower(text: str) -> str:
    """Alias for `str.lower`"""
    return text.lower()


@string_set.register
def to_upper(text: str) -> str:
    """Alias for `str.upper`"""
    return text.upper()


@string_set.register
def truncate(text: str, width, placeholder: str = '...') -> str:
    """Truncate text if longer than the specified width."""
    max_width = width - len(placeholder)
    return text if len(text) <= width else f'{text[:max_width]}{placeholder}'


@string_set.register
def truncate_word(text: str, width, placeholder: str = '...') -> str:
    """Alias for `textwrap.shorten`"""
    return textwrap.shorten(text, width, placeholder=placeholder)


@string_set.register
def zfill(text: str, width: int) -> str:
    """Alias for `str.zfill`"""
    return text.zfill(width)


#  _     _             _
# | |__ | |_ _ __ ___ | |
# | '_ \| __| '_ ` _ \| |
# | | | | |_| | | | | | |
# |_| |_|\__|_| |_| |_|_|
#

html_set = DefinitionSet()


@html_set.register
def html_escape(text: str, quote: bool = True) -> str:
    """Alias for `html.escape`"""
    return html.escape(text, quote)


@html_set.register
def html_unescape(text: str) -> str:
    """Alias for `html.unescape`"""
    return html.unescape(text)


#  _                     __   _  _
# | |__   __ _ ___  ___ / /_ | || |
# | '_ \ / _` / __|/ _ \ '_ \| || |_
# | |_) | (_| \__ \  __/ (_) |__   _|
# |_.__/ \__,_|___/\___|\___/   |_|
#

base64_set = DefinitionSet()


@base64_set.register
def standard_b64encode(plaintext: str) -> str:
    """Alias for `base64.standard_b64encode`"""
    return base64.standard_b64encode(plaintext.encode()).decode()


@base64_set.register
def standard_b64decode(encoded_text: str) -> str:
    """Alias for `base64.standard_b64decode`"""
    return base64.standard_b64decode(encoded_text.encode()).decode()


@base64_set.register
def urlsafe_b64encode(plaintext: str) -> str:
    """Alias for `base64.urlsafe_b64encode`"""
    return base64.urlsafe_b64encode(plaintext.encode()).decode()


@base64_set.register
def urlsafe_b64decode(encoded_text: str) -> str:
    """Alias for `base64.urlsafe_b64decode`"""
    return base64.urlsafe_b64decode(encoded_text.encode()).decode()


#  __  __       _
# |  \/  | __ _(_)_ __
# | |\/| |/ _` | | '_ \
# | |  | | (_| | | | | |
# |_|  |_|\__,_|_|_| |_|
#

_definition_sets = {
    'base64': base64_set,
    'html': html_set,
    'string': string_set,
}

main_set = DefinitionSet({
    'true': True,
    'false': False,
    'null': None,
})


@main_set.register(name='!')
@with_env
def python_exec(env: dict, code: str) -> str:
    """
    The single `!` macro simply executes the main text input as python code.

    To print to the output space at the same location the macro appear in,
    the python code must write to the `StringIO` object called `buffer`
    which will temporarily be injected into the environment of each macro call.
    For example,

    ```plain
    @!##{
        print("Hello, World!, file=buffer)
    }##
    ```
    """
    # Create a new buffer and inject into environment
    buffer = io.StringIO()
    env['buffer'] = buffer

    # Execute python code
    code = inspect.cleandoc(code)
    exec(code, env)

    # Remove buffer from environment, close it, and return its content
    del env['buffer']
    text = buffer.getvalue()
    buffer.close()
    return text


@main_set.register(name='load!')
@with_env
def load_definition_set(env: dict, name: str):
    """
    The `load!` macro which loads a set of extra definitions
    (values and functions) into the environment.

    Available sets are `string`, `html`, and `base64`.
    """
    try:
        one_set = _definition_sets[name.strip()]
    except KeyError as exc:
        available_list = ', '.join(_definition_sets.keys())
        raise PaxterTransformError(
            f"unrecognized definition set name {name.strip()!r} "
            f"(available are {available_list})",
        ) from exc
    env.update(one_set.data)
    return ''


@main_set.register(name='if')
@with_node
def process_if(transformer: 'SimpleSnakeTransformer', env: dict, node: PaxterFunc):
    """
    Paxter function expression of the form `@if[<test>,<bool>]{...}`
    is a special if-statement pattern in **Simple Snake**.

    The `<bool>` part must either be exactly the literal `true` or `false`.
    If this part is absent as in `@if[<test>]{...}`, then `true` will be assumed.

    The `<test>` part must be an identifier which will be tested for truthiness.
    If it is a callable, then it will be invoked first without arguments.

    When the `<test>` part is evaluated for truthiness,
    its result with be compared with `<bool>` part.
    Then the main text will be evaluated if and only if the comparison matches.
    """
    options: List[KeyValue] = node.options or []
    if not 1 <= len(options) <= 2:
        raise PaxterTransformError(
            "if condition at {pos} requires 1 or 2 options "
            "in the form [<test>] or [<test>,<bool>]",
            positions={'pos': node.start_pos},
        )

    if len(options) > 1:
        target_literal = options[1].get_faux_key()
        if target_literal == 'true':
            target_bool = True
        elif target_literal == 'false':
            target_bool = False
        else:
            raise PaxterTransformError(
                "second argument of if condition at {pos} "
                "must either be 'true' or 'false' literal",
                positions={'pos': node.start_pos},
            )
    else:
        target_bool = True

    test_id = options[0].get_faux_key()
    test = eval(test_id, env)
    if callable(test):
        test = test()

    if bool(test) is target_bool:
        return transformer.visit_fragment_list(env, node.fragments)
    else:
        return ''


@main_set.register(name='for')
@with_node
def process_for(transformer: 'SimpleSnakeTransformer', env: dict, node: PaxterFunc):
    """
    Paxter function expression of the form `@for[<item_id>,<seq>]{...}`
    is a special for-statement pattern in **Simple Snake**.

    The identifier presented at the `<item_id>` part will bind to
    each item produced by the identifier at the `<seq>` part,
    which will appear in the environment while evaluating the main text.

    The main text will be repeatedly evaluated for each item in `<seq>`,
    and the final result will be the concatenation of the evaluated result
    of the main text from each loop iteration.
    """
    options: List[KeyValue] = node.options or []
    if len(options) != 2:
        raise PaxterTransformError(
            "for loop at {pos} requires exactly 2 options "
            "in the form [<item_id>,<seq>]",
            positions={'pos': node.start_pos},
        )

    item_id = options[0].get_faux_key()
    seq = eval(options[1].get_faux_key(), env)

    fragments = []
    for value in seq:
        env[item_id] = value
        transformed = transformer.visit_fragment_list(env, node.fragments)
        fragments.append(transformed)

    return ''.join(fragments)
