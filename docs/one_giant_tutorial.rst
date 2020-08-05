##################
One Giant Tutorial
##################

Installation
============

Paxter python package can be installed from PyPI via ``pip`` command
(or any other methods of your choice):

.. code-block:: bash

   $ pip install paxter

----

Write a First Blog Entry
========================

While not required, Paxter package provides a set of data classes
that users can use to construct a rich document.
Here suppose that we are going to write a simple blog entry
using a few data classes from :mod:`paxter.authoring` subpackage.

.. code-block:: python

   from paxter.authoring import Bold, Link, Paragraph, line_break

   paragraph = Paragraph([
       "Hi, my name is ",
       Bold(["Ashley"]),
       line_break,
       "\nand my blog is located ",
       Link(["here"], "https://example.com"),
       ".",
   ])

.. code-block:: pycon

   >>> print(paragraph.html())
   <p>Hi, my name is <b>Ashley</b><br />
   and my blog is located <a href="https://example.com">here</a>.</p>

.. important::

   Everything located under the subpackage :mod:`paxter.authoring`
   are supplementary to but independent of the core Paxter library package.

Of course, this approach to writing documents
right inside python code space would be very cumbersome.
So Paxter library provides an alternative way to construct the exact same document.

.. code-block:: python

   from paxter.authoring import create_document_env
   from paxter.preset import run_simple_paxter

   # The following input text is written in-code for a simpler example.
   # However in reality, input text may be read from other sources
   # such as text files, some databases, or even fetched via some API.

   input_text = '''@paragraph{Hi, my name is @bold{Ashley}@break
   and my blog is located @link["https://example.com"]{here}.}'''
   env = create_document_env()
   document = run_simple_paxter(input_text, env)

.. code-block:: pycon

   >>> document
   [
       Paragraph(children=[
           'Hi, my name is ',
           Bold(children=['Ashley']),
           RawElement(children='<br />'),
           '\nand my blog is located ',
           Link(children=['here'], href='https://example.com'),
           '.',
       ]),
   ]
   >>> document[0] == paragraph
   True
   >>> print(document[0].html())
   <p>Hi, my name is <b>Ashley</b><br />
   and my blog is located <a href="https://example.com">here</a>.</p>

.. note::

   If readers are wondering why the resulting document
   is a list of :class:`Paragraph <paxter.authoring.document.Paragraph>`
   instance rather than just the instance itself,
   just be patient; we will discuss about this in upcoming sections.


Understanding commands
----------------------

Parts that begin with an ‘**@**’ symbol in Paxter input text
(e.g. ``@paragraph``, ``@bold``, ``@break``, and ``@link``)
are known as **commands** in Paxter language.
Commands can either be in the standalone form (like how ``@break`` appears)
or, when followed by at least one of ``[options]`` or ``{main argument}``,
it simulates a function call over such object.

For example, ``@bold{Ashley}`` in Paxter input text
is roughly equivalent to the python code ``bold(["Ashley"])``
which would be evaluated into ``Bold(children=["Ashley"])`` in the final result.
Similarly, 

.. code-block:: paxter

   @link["https://example.com"]{here}

would roughly be parsed into the following python code

.. code-block:: python

   link(["here"], "https://example.com")

which would then be evaluated into

.. code-block:: python

   Link(children=['here'], href='https://example.com')

Notice that the textual content
that is surrounded by *a matching pair of curly braces*
is always parsed into a list of values
and it always becomes the very first argument of translated function calls.
We call this part the **main argument** of a command.

Moreover, if we look at how the outermost ``@paragraph`` command is constructed,
we would see that the content of main argument
would always be *recursively parsed* into a list of values.
Hence, the above particular ``@paragraph`` command is in fact
roughly parsed into an equivalent python code as follows.

.. code-block:: python

   paragraph([
       "Hi, my name is ",
       bold(["Ashley"]),
       break_,
       "\nand my blog is located ",
       link(["here"], "https://example.com"),
       ".",
   ])

Now let us revisit the ``@link`` command from above once again.

.. code-block:: paxter

   @link["https://example.com"]{here}

Part of the command between *a matching pair of square brackets*
becomes the subsequent arguments of the ``link`` function call after the first.
This part is called the **options** of a command.
In fact, we can specify more than one value (argument) inside the options,
and all of these values will become the second argument, the third argument,
and so on.

For example, a Paxter command ``@foo["bar", 3]{main argument}``
would turn into the following equivalent python code.

.. code-block:: python

   foo(["main argument"], "bar", 3)

Python-style keyword arguments are also supported within the options.
For instance, a Paxter command ``@foo["bar", n=3]{main argument}`` gets turned into:

.. code-block:: python

   foo(["main argument"], "bar", n=3)

In addition, the main argument discussed earlier is actually *not* mandatory.
When it goes missing, all values with the options then
become sole arguments of the function call.
Therefore, this command ``@foo["bar", n=3]`` would simply be parsed into

.. code-block:: python

   foo("bar", n=3)

As a special case, to make a function call to a command with zero arguments,
simply write a pair of square brackets without anything inside it
(e.g. ``@foo[]``).

.. important::

   Finally, do take note that the main argument and the options of a command
   only try to mimic function call patterns in python;
   it actually does *not* fully support python syntax inside it.
   The full description of what is supported by Paxter language
   is discussed in :doc:`Paxter Language Tutorial <paxter_language_tutorial>` page.


Understanding environments
--------------------------

At this point, please note that ``@paragraph``, ``@bold``, and ``@link``
are merely aliases to the constructors of actual data classes
:class:`Paragraph <paxter.authoring.document.Paragraph>`,
:class:`Bold <paxter.authoring.document.Bold>`,
and :class:`Link <paxter.authoring.document.Link>` respectively.
These relationships are evident once we inspect
the content of the environment dictionary ``env`` (shown below).
Additionally, ``@break`` simply maps to the value
``RawElement(children='<br />')``.

.. code-block:: pycon

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

There is nothing preventing you from creating different environment mapping like so.

.. code-block:: python

   from paxter import authoring
   from paxter.authoring.standards import starter_unsafe_eval
   from paxter.preset import run_simple_paxter

   alternative_env = {
       # _starter_eval_ is required, but ignore this part for now
       '_starter_eval_': starter_unsafe_eval,
       'p': authoring.Paragraph,
       'b': authoring.Bold,
       'a': authoring.Link,
       'br': authoring.line_break
   }

   input_text = '''@p{Hi, my name is @b{Ashley}@br
   and my blog is located @a["https://example.com"]{here}.}'''
   document = run_simple_paxter(input_text, alternative_env)

.. code-block:: pycon

   >>> print(document[0].html())
   <p>Hi, my name is <b>Ashley</b><br />
   and my blog is located <a href="https://example.com">here</a>.</p>

----

.. todo::

   Continue here.


Add a Second Paragraph
======================

In the previous demonstration,
we have written a blog entry with a single paragraph,
but it was way too short.
So we will add another one.

.. code-block:: python

   from paxter.authoring import create_document_env
   from paxter.preset import run_simple_paxter

   input_text = '''@paragraph{Hi, my name is @bold{Ashley}@break
   and my blog is located @link["https://example.com"]{here}.}

   @paragraph{This is another paragraph.}'''
   env = create_document_env()
   document = run_simple_paxter(input_text, env)

.. code-block:: pycon

   >>> document
   [
       Paragraph(children=[
           'Hi, my name is ',
           Bold(children=['Ashley']),
           RawElement(children='<br />'),
           '\nand my blog is located ',
           Link(children=['here'], href='https://example.com'),
           '.',
       ]),
       '\n\n',
       Paragraph(children=['This is another paragraph.']),
   ]

In order to render the ``document``, iterating over each element of the list
in order to call :meth:`html() <paxter.authoring.document.Element.html>` rendering method would be annoying
(not to mention that some elements are just plain strings).

Paxter authoring toolchain mitigates this problem by providing
a convenient data class called
:class:`Document <paxter.authoring.document.Document>`.
We will wrap the result from :func:`run_simple_paxter <paxter.preset.run_simple_paxter>` under
:class:`Document <paxter.authoring.document.Document>`
data class.

.. code-block:: python

   from paxter.authoring import Document

   input_text = '''@paragraph{Hi, my name is @bold{Ashley}@break
   and my blog is located @link["https://example.com"]{here}.}

   @paragraph{This is another paragraph.}'''
   env = create_document_env()
   document = Document(run_simple_paxter(input_text, env))

.. code-block:: pycon

   >>> print(document.html())
   <p>Hi, my name is <b>Ashley</b><br />
   and my blog is located <a href="https://example.com">here</a>.</p><p>This is another paragraph.</p>

Document helper class
---------------------

Better yet, because writing multiple paragraphs in a single document
is a very common task, so :class:`Document <paxter.authoring.document.Document>`
would automatically split its content into paragraphs
separated by two or more newline characters,
and each resulting paragraph will receive a wrapping under
:class:`Paragraph <paxter.authoring.document.Paragraph>` data class
unless its entirely is a single document element of other kind.

.. code-block:: python

   input_text = '''Hi, my name is @bold{Ashley}@break
   and my blog is located @link["https://example.com"]{here}.

   This is another paragraph.

   @bold{This is a third paragraph.}'''
   env = create_document_env()
   document = Document(run_simple_paxter(input_text, env))

.. code-block:: pycon

   >>> print(document.html())
   <p>Hi, my name is <b>Ashley</b><br />
   and my blog is located <a href="https://example.com">here</a>.</p><p>This is another paragraph.</p><b>This is a third paragraph.</b>

Watch out for the third paragraph above!
They are surrounded by ``<b>`` tag in the result,
but the enclosing ``<p>`` tag is missing.
In this case, the explicit ``@paragraph`` marking is required.

.. code-block:: python

   input_text = '''Hi, my name is @bold{Ashley}@break
   and my blog is located @link["https://example.com"]{here}.

   This is another paragraph.

   @paragraph{@bold{This is a third paragraph.}}'''
   env = create_document_env()
   document = Document(run_simple_paxter(input_text, env))

.. code-block:: pycon

   >>> print(document.html())
   <p>Hi, my name is <b>Ashley</b><br />
   and my blog is located <a href="https://example.com">here</a>.</p><p>This is another paragraph.</p><p><b>This is a third paragraph.</b></p>

----

Include an email address
========================

You might already have noticed that ‘**@**’ symbol has special meaning in Paxter language;
it acts as a switch which turns the subsequent piece of input into a command.
Therefore, if you wish to include ‘**@**’ string literal as-is
in the final output, an escape of some sort is required.

Except that Paxter language actually does *not* provide a way
to *escape* ‘**@**’ symbols per se.
However, there is a way around this.

But first, let’s revisit the content of the environment dictionary.

.. code-block:: pycon

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

Let’s focus on ``env['_symbols_']`` which seems to be
a mapping from single symbol characters to some values.
Paxter uses this information to perform what is called
**symbolic replacements** of a special kind of command.
That is, whenever an ‘**@**’ command character is immediately followed by
another symbol character, then this symbolic replacement occurs.

For example, ‘**@!**’ inside the input text will be replaced by ``env['_symbols_']['!']``
and ‘**@@**’ will be replaced by ``env['_symbols_']['@']``, etc.
Therefore, Paxter lets users use ‘**@@**’ to mimic the escaping of ‘**@**’ symbol
though the mechanisms of symbolic replacements.

.. code-block:: python

   from paxter.authoring import Document, create_document_env
   from paxter.preset import run_simple_paxter

   input_text = '''Hi, my name is @bold{Ashley}@break
   and my blog is located @link["https://example.com"]{here}.

   To reach me directly, send email to ashley@@example.com'''
   env = create_document_env()
   document = Document(run_simple_paxter(input_text, env))

.. code-block:: pycon

   >>> print(document.html())
   <p>Hi, my name is <b>Ashley</b><br />
   and my blog is located <a href="https://example.com">here</a>.</p><p>To reach me directly, send email to ashley@example.com</p>

Of course, you can modify this behavior as well by customizing
``env['_symbols_']`` to suit your needs.


Document shortcut
-----------------

By the way, the following python code seems to be a recurring pattern.

.. code-block:: python

   from paxter.authoring import Document, create_document_env
   from paxter.preset import run_simple_paxter

   input_text = ...
   env = create_document_env()
   document = Document(run_simple_paxter(input_text, env))

Hence, there is even a neater shortcut as follows

.. code-block:: python

   from paxter.preset import run_document_paxter

   input_text = ...
   document = run_document_paxter(input_text)

----

Define common constants
=======================

While you are writing a document,
you might end up writing the same phrase over-and-over again.
You wish that you could define that constant once and reuse it over-and-over again.li
Well you can, in a lot of different ways.


First method: prepare in advance
--------------------------------

The first method we are going to demonstrate to you
is to prepare the evaluation environment dictionary
so that it also includes information about additional aliases.
Luckily, this is as simple as create a custom dictionary
using :func:`create_document_env <paxter.authoring.environ.create_document_env>`
and supply it as the second optional argument of the function
:func:`run_document_paxter <paxter.preset.run_document_paxter>`.

.. code-block:: python

   from paxter.authoring import create_document_env
   from paxter.preset import run_document_paxter

   env = create_document_env({
       'yaa': "Yet Another Acronym",
   })
   input_text = '''
   YAA is @yaa and it stands for @yaa.
   '''
   document = run_document_paxter(input_text, env)

.. code-block:: pycon

   >>> print(document.html())
   <p>YAA is Yet Another Acronym and it stands for Yet Another Acronym.</p>
   >>> env
   {'_starter_eval_': <function paxter.authoring.standards.starter_unsafe_eval(starter: str, env: dict) -> Any>,
    'for': DirectApply(wrapped=<function for_statement at 0x7f6a4e396ca0>),
    'if': DirectApply(wrapped=<function if_statement at 0x7f6a4e396dc0>),
    'python': DirectApply(wrapped=<function python_unsafe_exec at 0x7f6a4e361550>),
    'verb': <function paxter.authoring.standards.verbatim(text: Any) -> str>,
    'flatten': <function paxter.authoring.standards.flatten(data, join: bool = False) -> Union[List[str], str]>,
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
    'bulleted_list': paxter.authoring.document.BulletedList,
    'yaa': 'Yet Another Acronym'}

Observe that the command ``@yaa`` could be referred to inside input text
because the alias ``yaa`` maps to the string ``"Yet Another Acronym"``
inside the evaluation environment (as shown above).


Second method: inject python code
---------------------------------

Another method we are going to show you is to directly define
a new python variable right within the document itself.

You can embed any python code for execution right inside the input text
by wrapping python code with the ``@python`` command.
However, instead of putting your python code between a pair of braces,
replace those pair of braces with a pair of quotation marks instead.

.. code-block:: python

   from paxter.preset import run_document_paxter

   input_text = '''
   @python"yaa = 'Yet Another Acronym'"
   YAA is @yaa and it stands for @yaa.
   '''
   document = run_document_paxter(input_text)

.. code-block:: pycon

   >>> print(document.html())
   <p>YAA is Yet Another Acronym and it stands for Yet Another Acronym.</p>

It might seem crazy at first,
but this is one of very powerful features of Paxter package.

And suppose that you manually create the environment dictionary by yourself.
Below is what happens to the environment after execution.

.. code-block:: python

   from paxter.authoring import create_document_env
   from paxter.preset import run_document_paxter

   input_text = '''
   @python"yaa = 'Yet Another Acronym'"
   YAA is @yaa and it stands for @yaa.
   '''
   env = create_document_env()
   document = run_document_paxter(input_text, env)

.. code-block:: pycon

   >>> print(document.html())
   <p>YAA is Yet Another Acronym and it stands for Yet Another Acronym.</p>
   >>> env
   {'_starter_eval_': <function paxter.authoring.standards.starter_unsafe_eval(starter: str, env: dict) -> Any>,
    'for': DirectApply(wrapped=<function for_statement at 0x7f9c76ea3af0>),
    'if': DirectApply(wrapped=<function if_statement at 0x7f9c76ea3c10>),
    ...
    'yaa': 'Yet Another Acronym'}

The mapping of ``yaa`` gets entered into the environment dictionary!
This happened because the command ``@python`` called
``exec()`` built-in function behind the scenes
with ``env`` as the global dictionary.


Quoted main argument?
~~~~~~~~~~~~~~~~~~~~~

You might have asked,
*why wrapping the main argument of a command with a pair of a quotation mark instead of a pair of curly braces? Is this a totally new syntax I have to remember?*

Not quite. By using quotation marks instead of curly braces,
we merely modifies the parsing behavior of the main argument.
To highlight the difference between two parsing modes,
let’s look at how the above ``@python`` command got parsed.

Specifically, ``@python"yaa = 'Yet Another Acronym'"``
will be equivalent to the following python code.

.. code-block:: python

   python("yaa = 'Yet Another Acronym")

Here, the main argument no longer gets parsed into a list.
It is just a plain string!
This also has some quirky implications as well:
it is *impossible* to nest a command with the *quoted* main argument
(which also means that you also do not need to escape ‘**@**’
like what we have done to email address previously).

But what if we wish to include quotation marks as
part of the textual content of the quoted main argument?
How do we *escape* quotation marks?
As you might have learned so far,
Paxter does not implement character escaping mechanism of any sorts.
Instead we adopted Rust raw-string syntax in Paxter:
by enclosing the string literal with an equal number of hash characters!

.. code-block:: python

   from paxter.preset import run_document_paxter

   input_text = '''
   @python##"yaa = "Yet Another Acronym""##
   YAA is @yaa and it stands for @yaa.
   '''
   document = run_document_paxter(input_text)

.. code-block:: pycon

   >>> print(document.html())
   <p>YAA is Yet Another Acronym and it stands for Yet Another Acronym.</p>

We have not told you earlier that this hash-enclosing mechanisms
works with main argument surrounded by curly braces as well!
For example, ``@foo##{Natural numbers are {0, 1, 2, ...}.}##``
will be parsed roughly to the following python code.

.. code-block:: python

   foo(["Natural numbers are {0, 1, 2, ...}."])

.. todo::

   More stuff coming soon (under construction).
