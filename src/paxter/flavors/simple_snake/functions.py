"""
Collection of readily available functions
in the initial environment dictionary.
"""
import base64
import html
import inspect
import textwrap
from typing import Optional

from paxter.helpers.environ import Environ

default_env = Environ({
    'null': None,
    'true': True,
    'false': False,
})


#  __  __
# |  \/  | __ _  ___ _ __ ___
# | |\/| |/ _` |/ __| '__/ _ \
# | |  | | (_| | (__| | | (_) |
# |_|  |_|\__,_|\___|_|  \___/
#

@default_env.register_macro(name='!')
def python_exec(env: dict, statements: str) -> str:
    """
    Invoke the given python statements for effect
    and then return empty string.
    """
    exec(statements, env)
    return ""


#  ____  _        _
# / ___|| |_ _ __(_)_ __   __ _
# \___ \| __| '__| | '_ \ / _` |
#  ___) | |_| |  | | | | | (_| |
# |____/ \__|_|  |_|_| |_|\__, |
#                         |___/

@default_env.register_func
def capitalize(text: str) -> str:
    return text.capitalize()


@default_env.register_func
def casefold(text: str) -> str:
    return text.casefold()


@default_env.register_func(name='centering')
def center(text: str, width: int, fillchar: str = ' ') -> str:
    return text.center(width, fillchar)


@default_env.register_func
def expandtabs(text: str, tabsize: int = 8) -> str:
    return text.expandtabs(tabsize)


@default_env.register_func
def ljust(text: str, width: int, fillchar: str = ' ') -> str:
    return text.ljust(width, fillchar)


@default_env.register_func(name='to_lower')
def lower(text: str) -> str:
    return text.lower()


@default_env.register_func
def lstrip(text: str, chars: Optional[str] = None) -> str:
    return text.lstrip(chars)


@default_env.register_func
def replace(text: str, old: str, new: str, count: int = -1) -> str:
    return text.replace(old, new, count)


@default_env.register_func
def rjust(text: str, width: int, fillchar: str = ' ') -> str:
    return text.rjust(width, fillchar)


@default_env.register_func
def rstrip(text: str, chars: Optional[str] = None) -> str:
    return text.rstrip(chars)


@default_env.register_func
def strip(text: str, chars: Optional[str] = None) -> str:
    return text.strip(chars)


@default_env.register_func
def swapcase(text: str) -> str:
    return text.swapcase()


@default_env.register_func
def maketitle(text: str) -> str:
    return text.title()


@default_env.register_func(name='to_upper')
def upper(text: str) -> str:
    return text.upper()


@default_env.register_func
def zfill(text: str, width: int) -> str:
    return text.zfill(width)


#  _     _             _
# | |__ | |_ _ __ ___ | |
# | '_ \| __| '_ ` _ \| |
# | | | | |_| | | | | | |
# |_| |_|\__|_| |_| |_|_|
#

@default_env.register_func
def html_escape(text: str, quote: bool = True) -> str:
    return html.escape(text, quote)


@default_env.register_func
def html_unescape(text: str) -> str:
    return html.unescape(text)


#  _                     __   _  _
# | |__   __ _ ___  ___ / /_ | || |
# | '_ \ / _` / __|/ _ \ '_ \| || |_
# | |_) | (_| \__ \  __/ (_) |__   _|
# |_.__/ \__,_|___/\___|\___/   |_|
#

@default_env.register_func
def standard_b64encode(plaintext: str) -> str:
    return base64.standard_b64encode(plaintext.encode()).decode()


@default_env.register_func
def standard_b64decode(encoded_text: str) -> str:
    return base64.standard_b64decode(encoded_text.encode()).decode()


@default_env.register_func
def urlsafe_b64encode(plaintext: str) -> str:
    return base64.urlsafe_b64encode(plaintext.encode()).decode()


@default_env.register_func
def urlsafe_b64decode(encoded_text: str) -> str:
    return base64.urlsafe_b64decode(encoded_text.encode()).decode()


#  _            _
# | |_ _____  _| |___      ___ __ __ _ _ __
# | __/ _ \ \/ / __\ \ /\ / / '__/ _` | '_ \
# | ||  __/>  <| |_ \ V  V /| | | (_| | |_) |
#  \__\___/_/\_\\__| \_/\_/ |_|  \__,_| .__/
#                                     |_|

@default_env.register_func
def indent(text: str, prefix: str) -> str:
    return textwrap.indent(text, prefix)


@default_env.register_func
def dedent(text: str) -> str:
    return textwrap.dedent(text)


@default_env.register_func
def cleandoc(text: str) -> str:
    return inspect.cleandoc(text)


@default_env.register_func
def linewrap(text: str, width: int = 70) -> str:
    return textwrap.fill(text, width)


@default_env.register_func
def truncate_word(text: str, width, placeholder: str = '...') -> str:
    return textwrap.shorten(text, width, placeholder=placeholder)


@default_env.register_func
def truncate(text: str, width, placeholder: str = '...') -> str:
    max_width = width - len(placeholder)
    return text if len(text) <= width else f'{text[:max_width]}{placeholder}'
