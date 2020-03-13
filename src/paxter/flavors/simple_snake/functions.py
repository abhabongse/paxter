"""
## List of Available Functions

### Function Set `string`

Available functions are `capitalize`, `casefold`, `centering`, `dedent`, `expandtabs`,
`indent`, `linewrap`, `ljust`, `lstrip`, `maketitle`, `replace`, `rjust`, `rstrip`,
`strip`, `swapcase`, `to_lower`, `to_upper`, `truncate`, `truncate_word`, and `zfill`.

### Function Set `html`

Available functions are `html_escape` and `html_unescape`.

### Function Set `base64`

Available functions are `standard_b64encode`, `standard_b64decode`,
`urlsafe_b64encode`, and `urlsafe_b64decode`.
"""
import base64
import html
import inspect
import textwrap
from typing import Optional

from paxter.flavors.simple_snake._envset import EnvironSet

# TODO: Perhaps use `inspect` module to
#       automatically and efficiently redefine functions
# TODO: Make documentation automated

#  ____  _        _
# / ___|| |_ _ __(_)_ __   __ _
# \___ \| __| '__| | '_ \ / _` |
#  ___) | |_| |  | | | | | (_| |
# |____/ \__|_|  |_|_| |_|\__, |
#                         |___/

string_set = EnvironSet()


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

html_set = EnvironSet()


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

base64_set = EnvironSet()


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
