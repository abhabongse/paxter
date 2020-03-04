"""
A collection of regexp-based lexers for Paxter experimental language.
"""
import functools
import re
from typing import Pattern

#  _____ _ _
# |  ___| (_)_ __  _ __   ___ _ __ ___
# | |_  | | | '_ \| '_ \ / _ \ '__/ __|
# |  _| | | | |_) | |_) |  __/ |  \__ \
# |_|   |_|_| .__/| .__/ \___|_|  |___/
#           |_|   |_|

LEFT_CHARS = r'#<{"'
RIGHT_CHARS = r'#>}"'
LEFT_TO_RIGHT_TRANS = str.maketrans(LEFT_CHARS, RIGHT_CHARS)


def flip_pattern(lft_pattern: str) -> str:
    """
    Flips the given left (i.e. opening) pattern into its corresponding
    right (i.e. closing) pattern (such as `"<##<{"` into `"}>##>"`).
    """
    assert all(c in LEFT_CHARS for c in lft_pattern)
    return lft_pattern.translate(LEFT_TO_RIGHT_TRANS)[::-1]


#  _
# | |    _____  _____ _ __ ___
# | |   / _ \ \/ / _ \ '__/ __|
# | |__|  __/>  <  __/ |  \__ \
# |_____\___/_/\_\___|_|  |___/
#

PAXTER_MACRO_PREFIX_RE = re.compile(r'@(?P<id>\w*!)', flags=re.DOTALL)
PAXTER_FUNC_PREFIX_RE = re.compile(r'@(?P<id>\w+)', flags=re.DOTALL)
PAXTER_PHRASE_PREFIX_RE = re.compile(r'@[#<]*{', flags=re.DOTALL)
GLOBAL_BREAK_RE = re.compile(r'(?P<text>.*?)(?P<break>@|\Z)', flags=re.DOTALL)
LEFT_RE = re.compile(r'[#<]*{', flags=re.DOTALL)


@functools.lru_cache(maxsize=None)
def fragment_break_re(rgt_pattern: str) -> Pattern[str]:
    """
    Compiles a regular expression lexer to match some raw text non-greedily
    followed by either the @-symbol or the given right (i.e. closing) pattern.
    """
    escaped_pattern = re.escape(rgt_pattern)
    return re.compile(rf'(?P<text>.*?)(?P<break>@|{escaped_pattern})', flags=re.DOTALL)


@functools.lru_cache(maxsize=None)
def macro_break_re(rgt_pattern: str) -> Pattern[str]:
    """
    Compiles a regular expression lexer to match some raw text non-greedily
    followed by the given right (i.e. closing) pattern.
    """
    escaped_pattern = re.escape(rgt_pattern)
    return re.compile(rf'(?P<text>.*?)(?P<break>{escaped_pattern})', flags=re.DOTALL)

# TODO: add helper class consisting of (lexer, matchobj)
