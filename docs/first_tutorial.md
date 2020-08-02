# First Tutorial

## Installation

Paxter python package can be installed from PyPI via `pip` command
(or any other methods of your choice):

```bash
$ pip install paxter
```

## Write a first blog entry

While not required, Paxter package provides a set of data classes
that users can use to construct a rich document.
Here suppose that we are going to write a simple blog entry.

```python
from paxter.authoring import Bold, Link, Paragraph, line_break

paragraph = Paragraph([
    "Hi, my name is ",
    Bold(["Ashley"]),
    line_break,
    "\nand my blog is located at ",
    Link(["ashley.example.com"], "https://ashley.example.com")
])
```
```pycon
>>> print(paragraph.html())
<p>Hi, my name is <b>Ashley</b><br />
and my blog is located at <a href="https://ashley.example.com">ashley.example.com</a></p>
```

Of course, this method of writing documents inside python code would be very cumbersome.
So we have an alternative way to construct the exact same document.

```python
from paxter.authoring import create_document_env
from paxter.preset import run_paxter

input_text = '''@paragraph{Hi, my name is @bold{Ashley}@break
and my blog is located at @link["https://ashley.example.com"]{ashley.example.com}}'''
env = create_document_env()
document = run_paxter(input_text, env)
```

```pycon
>>> document
[
    Paragraph(children=[
        'Hi, my name is ',
        Bold(children=['Ashley']),
        RawElement(children='<br />'),
        '\nand my blog is located at ',
        Link(children=['ashley.example.com'], href='https://ashley.example.com')
    ]),
]
>>> document[0] == paragraph
True
>>> print(document[0].html())
<p>Hi, my name is <b>Ashley</b><br />
and my blog is located at <a href="https://ashley.example.com">ashley.example.com</a></p>
```

(If you are wondering why the resulting document is 
a list of a single `Paragraph` data class instance
instead of just the object itself,
just be patient and we will discuss this in a later section.)

### Understanding commands

`@paragraph`, `@bold`, `@break`, and `@link` 
from within the input text are called **commands**,
and when they are followed by at least one of `[options]` or `{main text}`
then they become function calls.

To put it simply, `@bold{Ashley}` in Paxter syntax 
is translated to the python code `bold(["Ashley"])`
before it is evaluated into final result `Bold(children=['Ashley'])`.
Similarly, 

```paxter
@link["https://ashley.example.com"]{ashley.example.com}
```

is roughly translated into the following python code

```python
link(["ashley.example.com"], "https://ashley.example.com")
```

and then it is evaluated into

```python
Link(children=['ashley.example.com'], href='https://ashley.example.com')
```

Notice that the textual content surrounded by a pair of curly braces
is always parsed into a list of values,
and it always becomes the very first argument of the function call.
We call this part the **main argument** of a command.

Moreover, if we look at how the outermost `paragraph` command is constructed,
we would notice that the main argument is also _recursively parsed_.
Hence, the input text is actually parsed into the following equivalent python code.

```python
paragraph([
    "Hi, my name is ",
    bold(["Ashley"]),
    break_,
    "\nand my blog is located at ",
    link(["ashley.example.com"], "https://ashley.example.com"),
])
```

Now let’s focus on the `link` command once again.
The part between a pair of square brackets
becomes the second argument of the `link` function call.
This part is called the **options** of a command.
In fact, we can specify more than one option to the command too.

For example, the Paxter command `@foo["bar", 3]{Main argument}`
would turn into the following equivalent python code:

```python
foo(["Main argument"], "bar", 3)
```

Python style keyword arguments are also supported inside options.
So the Paxter command `@foo["bar", n=3]{Main argument}` gets turned into:

```python
foo(["Main argument"], "bar", n=3)
```

However, options of a command only mimics Python function call pattern;
it does not support full python syntax inside it. 
The full description of what is supported in a command in general
is discussed in other pages.

```eval_rst
.. todo:: 

   Add links to other pages (under construction).
```


### Understanding environments

At this point, please note that `paragraph`, `bold`, and `link`
are merely aliases to the actual data classes `Paragraph`, `Bold`, and `Link`
due to the environment dictionary `env` (shown below).

```pycon
>>> env
{'_starter_eval_': <function paxter.authoring.standards.starter_unsafe_eval(starter: str, env: dict) -> Any>,
 'for': DirectApply(wrapped=<function for_statement at 0x7ff5ca9ff700>),
 'if': DirectApply(wrapped=<function if_statement at 0x7ff5ca9ff820>),
 'python': DirectApply(wrapped=<function python_unsafe_exec at 0x7ff5bbf40040>),
 'verb': <function paxter.authoring.standards.verbatim(text: Any) -> str>,
 'flatten': <function paxter.authoring.standards.flatten(data, join: bool = False) -> Union[List[str], str]>,
 '_symbols_': {'!': '',
  '@': '@',
  '.': RawElement(children='&hairsp;'),
  ',': RawElement(children='&thinsp;'),
  '%': RawElement(children='&nbsp;')},
 'raw': paxter.authoring.document.RawElement,
 'break': RawElement(children='<br />'),
 'hrule': RawElement(children='<hr />'),
 'nbsp': RawElement(children='&nbsp;'),
 'hairsp': RawElement(children='&hairsp;'),
 'thinsp': RawElement(children='&thinsp;'),
 'paragraph': paxter.authoring.document.Paragraph,
 'h1': paxter.authoring.document.Heading1,
 'h2': paxter.authoring.document.Heading2,
 'h3': paxter.authoring.document.Heading3,
 'h4': paxter.authoring.document.Heading4,
 'h5': paxter.authoring.document.Heading5,
 'h6': paxter.authoring.document.Heading6,
 'bold': paxter.authoring.document.Bold,
 'italic': paxter.authoring.document.Italic,
 'uline': paxter.authoring.document.Underline,
 'code': paxter.authoring.document.Code,
 'blockquote': paxter.authoring.document.Blockquote,
 'link': paxter.authoring.document.Link,
 'image': paxter.authoring.document.Image,
 'numbered_list': paxter.authoring.document.NumberedList,
 'bulleted_list': paxter.authoring.document.BulletedList}
```

There is nothing preventing you from creating different environment mapping like so.

```python
from paxter import authoring
from paxter.authoring.standards import starter_unsafe_eval
from paxter.preset import run_paxter

alternative_env = {
    # _starter_eval_ is required, but ignore this part for now
    '_starter_eval_': starter_unsafe_eval,
    'p': authoring.Paragraph,
    'b': authoring.Bold,
    'a': authoring.Link,
    'br': authoring.line_break
}

input_text = '''@p{Hi, my name is @b{Ashley}@br
and my blog is located at @a["https://ashley.example.com"]{ashley.example.com}}'''
document = run_paxter(input_text, alternative_env)
```

```pycon
>>> print(document[0].html())
<p>Hi, my name is <b>Ashley</b><br />
and my blog is located at <a href="https://ashley.example.com">ashley.example.com</a></p>
```


## Add a second paragraph

The blog entry with a single paragraph is way too short.
So we will add another one.

```python
from paxter.authoring import create_document_env
from paxter.preset import run_paxter

input_text = '''@paragraph{Hi, my name is @bold{Ashley}@break
and my blog is located at @link["https://ashley.example.com"]{ashley.example.com}}

@paragraph{This is another paragraph.}'''
env = create_document_env()
document = run_paxter(input_text, env)
```

```pycon
>>> document
[
    Paragraph(children=[
        'Hi, my name is ', 
        Bold(children=['Ashley']), 
        RawElement(children='<br />'),
        '\nand my blog is located at ', 
        Link(children=['ashley.example.com'], href='https://ashley.example.com')
    ]),
    '\n\n',
    Paragraph(children=['This is another paragraph.']),
]
```

It would be very annoying to iterate through each element of the `document`
to call `html()` rendering method (and some elements are even just strings).

Hence, Paxter also provides a convenient data class to mitigate this common situation:
we wrap the result from `run_paxter` under `Document` data class.

```python
from paxter.authoring import Document

input_text = '''@paragraph{Hi, my name is @bold{Ashley}@break
and my blog is located at @link["https://ashley.example.com"]{ashley.example.com}}

@paragraph{This is another paragraph.}'''
env = create_document_env()
document = Document(run_paxter(input_text, env))
```

```pycon
>>> print(document.html())
<p>Hi, my name is <b>Ashley</b><br />
and my blog is located at <a href="https://ashley.example.com">ashley.example.com</a></p><p>This is another paragraph.</p>
```

Better yet, because writing multiple paragraphs 
in a single document is an obvious and mundane tasks,
the `Document` data class will automatically split internal textual content
into paragraphs if they are separated by two or more newline characters.
Each split paragraph will receive a paragraph wrapping
unless its entirety is a single command.

```python
input_text = '''Hi, my name is @bold{Ashley}@break
and my blog is located at @link["https://ashley.example.com"]{ashley.example.com}

This is another paragraph.

@bold{This is a third paragraph.}'''
env = create_document_env()
document = Document(run_paxter(input_text, env))
```

```pycon
>>> print(document.html())
<p>Hi, my name is <b>Ashley</b><br />
and my blog is located at <a href="https://ashley.example.com">ashley.example.com</a></p><p>This is another paragraph.</p><b>This is a third paragraph.</b>
```

Watch out for the third paragraph above!
They are surrounded by `<b>` tag in the result,
but the `<p>` tag is missing. 
In this case, the explicit `@paragraph` marking is required.

```python
input_text = '''Hi, my name is @bold{Ashley}@break
and my blog is located at @link["https://ashley.example.com"]{ashley.example.com}

This is another paragraph.

@paragraph{@bold{This is a third paragraph.}}'''
env = create_document_env()
document = Document(run_paxter(input_text, env))
```

```pycon
>>> print(document.html())
<p>Hi, my name is <b>Ashley</b><br />
and my blog is located at <a href="https://ashley.example.com">ashley.example.com</a></p><p>This is another paragraph.</p><p><b>This is a third paragraph.</b></p>
```


## Include an email address

As you might have noticed, `@` symbol has special meaning in Paxter language.
Hence, to include `@` in the final output requires escaping.

Except that Paxter language does not provide you a way to escape `@` symbols at all.
However, there is a way around this.
But first, let’s revisit the content of the environment dictionary.

```pycon
>>> from paxter.authoring import create_document_env
>>> env = create_document_env()
>>> env
{'_starter_eval_': <function paxter.authoring.standards.starter_unsafe_eval(starter: str, env: dict) -> Any>,
 'for': DirectApply(wrapped=<function for_statement at 0x7f7d6ecb0700>),
 'if': DirectApply(wrapped=<function if_statement at 0x7f7d6ecb0820>),
 'python': DirectApply(wrapped=<function python_unsafe_exec at 0x7f7d5fa3e040>),
 'verb': <function paxter.authoring.standards.verbatim(text: Any) -> str>,
 'flatten': <function paxter.authoring.standards.flatten(data, join: bool = False) -> Union[List[str], str]>,
 '_symbols_': {'!': '',
  '@': '@',
  '.': RawElement(children='&hairsp;'),
  ',': RawElement(children='&thinsp;'),
  '%': RawElement(children='&nbsp;')},
 'raw': paxter.authoring.document.RawElement,
 'break': RawElement(children='<br />'),
 'hrule': RawElement(children='<hr />'),
 'nbsp': RawElement(children='&nbsp;'),
 'hairsp': RawElement(children='&hairsp;'),
 'thinsp': RawElement(children='&thinsp;'),
 'paragraph': paxter.authoring.document.Paragraph,
 'h1': paxter.authoring.document.Heading1,
 'h2': paxter.authoring.document.Heading2,
 'h3': paxter.authoring.document.Heading3,
 'h4': paxter.authoring.document.Heading4,
 'h5': paxter.authoring.document.Heading5,
 'h6': paxter.authoring.document.Heading6,
 'bold': paxter.authoring.document.Bold,
 'italic': paxter.authoring.document.Italic,
 'uline': paxter.authoring.document.Underline,
 'code': paxter.authoring.document.Code,
 'blockquote': paxter.authoring.document.Blockquote,
 'link': paxter.authoring.document.Link,
 'image': paxter.authoring.document.Image,
 'numbered_list': paxter.authoring.document.NumberedList,
 'bulleted_list': paxter.authoring.document.BulletedList}
```

Let’s focus on `env['_symbols_']` which seems to be 
a mapping from a single symbol character to some value.
Paxter uses this information to perform what is called **symbolic replacements**
of a special kind of command.

That is, whenever an `@` command character is immediately followed by 
another symbol character, then this symbolic replacement occurs.
For example, `@!` inside the input text will be replaced by `env['_symbols_']['!']`
and `@@` will be replaced by `env['_symbols_']['@']`, etc.
Therefore, Paxter uses `@@` to mimic the escaping of `@` symbol
though the mechanisms of symbolic replacements.

```python
from paxter.authoring import Document, create_document_env
from paxter.preset import run_paxter

input_text = '''Hi, my name is @bold{Ashley}@break
and my blog is located at @link["https://ashley.example.com"]{ashley.example.com}

To reach me directly, send email to ashley@@example.com'''
env = create_document_env()
document = Document(run_paxter(input_text, env))
```

```pycon
>>> print(document.html())
<p>Hi, my name is <b>Ashley</b><br />
and my blog is located at <a href="https://ashley.example.com">ashley.example.com</a></p><p>To reach me directly, send email to ashley@example.com</p>
```

Of course, you can modify this behavior as well by customizing
`env['_symbols_']` to suit your needs.


## Define common constants

```eval_rst
.. todo:: 

   More stuff coming soon (under construction).
```
