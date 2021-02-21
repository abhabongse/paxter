# Disable Python Environment (Demo)

In this demo, we are going to customize the initial environment dictionary
in order to prevent arbitrary python code execution whatsoever.
Perhaps we as a programmer would like our users to write some content
using Paxter language without any risk of arbitrary code execution.

By default, the initial environment dictionary created by
{func}`create_document_env() <paxter.authoring.environ.create_document_env>`
allows python code execution through two distinct endpoints:

- the {func}`@python <paxter.authoring.standards.python_unsafe_exec>` command
- the anonymous python expression evaluation of phrase part of a command
  (which is dictated by the function 
  {func}`python_unsafe_eval() <paxter.authoring.standards.python_unsafe_eval>` 
  located at `env["_phrase_eval_"]` of the environment `env`)

For the first endpoint, we simply remove the command from the environment,
whereas for the second endpoint, we replace the function 
located at `env["_phrase_eval_"]` with another variant 
that does not make a call to {func}`eval` built-in function.

```python
from typing import Optional

from paxter.quickauthor.controls import for_statement, if_statement
from paxter.quickauthor.elements import (
  Blockquote, Bold, BulletedList, Code,
  Heading1, Heading2, Heading3, Heading4, Heading5, Heading6,
  Image, Italic, Link, NumberedList, Paragraph, RawElement,
  Table, TableHeader, TableRow, Underline,
  hair_space, horizontal_rule, line_break,
  non_breaking_space, thin_space,
)
from paxter.quickauthor.standards import verbatim


def phrase_safe_eval(phrase: str, env: dict) -> Any:
  """
  Safely evaluates the given phrase of a command.
  If performs the evaluation in the following order.

  1. Looks up the value from ``env['_extras_']`` dict using phrase as key
  2. Looks up the value from ``env`` dict using phrase as key.

  The implementation of this function is borrowed from inspecting
  :func:`paxter.authoring.standards.phrase_unsafe_eval`.
  """
  if not phrase:
    return None
  extras = env.get('_extras_', {})
  if phrase in extras:
    return extras[phrase]
  if phrase in env:
    return env[phrase]
  raise KeyError(f"there is no command with key: {phrase}")


def create_safe_document_env(data: Optional[dict] = None):
  """
  Creates an string environment data for Paxter source code evaluation
  in Python authoring mode, specializes in constructing documents.

  The implementation of this function is borrowed from inspecting
  :func:`paxter.authoring.environ.create_document_env`.
  """
  data = data or {}
  return {
    '_phrase_eval_': phrase_safe_eval,
    '_extras_': {},
    '@': '@',
    'for': for_statement,
    'if': if_statement,
    # 'python': python_unsafe_exec,
    'verb': verbatim,
    'raw': RawElement,
    'paragraph': Paragraph.from_fragments,
    'h1': Heading1.from_fragments,
    'h2': Heading2.from_fragments,
    'h3': Heading3.from_fragments,
    'h4': Heading4.from_fragments,
    'h5': Heading5.from_fragments,
    'h6': Heading6.from_fragments,
    'bold': Bold.from_fragments,
    'italic': Italic.from_fragments,
    'uline': Underline.from_fragments,
    'code': Code.from_fragments,
    'blockquote': Blockquote.from_fragments,
    'link': Link.from_fragments,
    'image': Image,
    'numbered_list': NumberedList.from_direct_args,
    'bulleted_list': BulletedList.from_direct_args,
    'table': Table.from_direct_args,
    'table_header': TableHeader.from_direct_args,
    'table_row': TableRow.from_direct_args,
    'hrule': horizontal_rule,
    'line_break': line_break,
    '\\': line_break,
    'nbsp': non_breaking_space,
    '%': non_breaking_space,
    'hairsp': hair_space,
    '.': hair_space,
    'thinsp': thin_space,
    ',': thin_space,
    **data,
  }
```

And now we may safely evaluate the content written in Paxter language
without having to worry that there may be arbitrary python code execution
by using the initial environment dictionary created by the function
`create_safe_document_env()` from above.

```python
from paxter.quickauthor import run_document_paxter

# The following source text is read from a source file.
# However, in reality, source text may be read from other sources
# such as some databases or even fetched via some content management API.
with open("new-blog.paxter") as fobj:
  source_text = fobj.read()

env = create_safe_document_env()  # from above
document = run_document_paxter(source_text, env)
html_output = document.html()
```
