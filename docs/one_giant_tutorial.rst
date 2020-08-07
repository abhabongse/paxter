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

   from paxter.authoring.document import Bold, Link, Paragraph, line_break

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

   from paxter.authoring import create_document_env, run_simple_paxter

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

Notice that the textual content,
surrounded by *a matching pair of curly braces*,
is always parsed into a list of values.
Moreover, the parsed list would always be positioned
as the very first argument of translated function calls.
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

For example, the Paxter command ``@foo["bar", 3]{main argument}``
would turn into the following equivalent python code.

.. code-block:: python

   foo(["main argument"], "bar", 3)

Python-style keyword arguments are also supported within the options.
For instance, the Paxter command ``@foo["bar", n=3]{main argument}`` gets turned into:

.. code-block:: python

   foo(["main argument"], "bar", n=3)

In addition, the main argument discussed earlier is actually *not* mandatory.
When it is absent, all values within the options then
become sole arguments of the function call.
Therefore, the command ``@foo["bar", n=3]`` would simply be parsed into

.. code-block:: python

   foo("bar", n=3)

As a special case, to make a function call with zero arguments from a command,
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

There is nothing preventing library users
from creating different environment mapping like so.

.. code-block:: python

   from paxter.authoring import document, run_simple_paxter, standards

   alternative_env = {
       # _starter_eval_ is required, but ignore this part for now
       '_starter_eval_': standards.starter_unsafe_eval,
       'p': document.Paragraph,
       'b': document.Bold,
       'a': document.Link,
       'br': document.line_break
   }

   input_text = '''@p{Hi, my name is @b{Ashley}@br
   and my blog is located @a["https://example.com"]{here}.}'''
   document = run_simple_paxter(input_text, alternative_env)

.. code-block:: pycon

   >>> print(document[0].html())
   <p>Hi, my name is <b>Ashley</b><br />
   and my blog is located <a href="https://example.com">here</a>.</p>

----

Add a Second Paragraph
======================

In the previous section,
we have written a blog entry with a single paragraph,
but it was way too short.
So we will add another one.

.. code-block:: python

   from paxter.authoring import create_document_env, run_simple_paxter

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

Because the resulting ``document`` (shown above)
is a list of :class:`str` or :class:`Element <paxter.authoring.document.Element>` instances
(from which :class:`Paragraph <paxter.authoring.document.Paragraph>` is derived),
in order to render the final HTML result,
we have to take the effort to iterate over each member of the list.
Fortunately, there is a better way.


Document helper class
---------------------

Subpackage :mod:`paxter.authoring.document` provides a convenient data class called
:class:`Document <paxter.authoring.document.Document>`
to wrap over the list returned by :func:`run_simple_paxter <paxter.authoring.preset.run_simple_paxter>`.

.. code-block:: python

   from paxter.authoring import create_document_env, run_simple_paxter
   from paxter.authoring.document import Document

   input_text = '''@paragraph{Hi, my name is @bold{Ashley}@break
   and my blog is located @link["https://example.com"]{here}.}

   @paragraph{This is another paragraph.}'''
   env = create_document_env()
   document = Document(run_simple_paxter(input_text, env))

.. code-block:: pycon

   >>> print(document.html())
   <p>Hi, my name is <b>Ashley</b><br />
   and my blog is located <a href="https://example.com">here</a>.</p><p>This is another paragraph.</p>

Better yet, because writing multiple paragraphs in a single document is too common,
we do *not* need to explicitly annotate each paragraph with ``@paragraph`` command;
the :class:`Document <paxter.authoring.document.Document>` class
will automatically split its content into paragraphs
separated by two or more newline characters,
and each resulting paragraph will receive a wrapping under
:class:`Paragraph <paxter.authoring.document.Paragraph>` data class
unless its entirely is a single :class:`Element <paxter.authoring.document.Element>` of other kinds.

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

Include an Email Address
========================

As readers have already noticed that ‘**@**’ symbol has special meaning in Paxter language:
it acts as a switch which turns the subsequent piece of input into a command.
Therefore, if library users wish to include ‘**@**’ string literal as-is
in the final output, an escape of some sort is required.

Except that Paxter language actually does *not* provide a way
to *escape* ‘**@**’ symbols per se.
However, there is a way around this.

But first, let us revisit the content of the environment dictionary once again.

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

Let us focus on ``env['_symbols_']`` which seems to be
a mapping from single symbol characters to some values.
Paxter uses this information to perform what is called **symbolic replacements**.
That is, whenever an ‘**@**’ character
is immediately followed by *another symbol character*,
then this symbolic replacement occurs.

For example, ``@!`` inside the input text will be replaced by ``env['_symbols_']['!']``
whereas ``@@`` will be replaced by ``env['_symbols_']['@']``, etc.
Therefore, Paxter lets users use ``@@`` to mimic the escaping of ‘**@**’ symbol
though the mechanisms of symbolic replacements.

.. code-block:: python

   from paxter.authoring import create_document_env, run_simple_paxter
   from paxter.authoring.document import Document

   input_text = '''Hi, my name is @bold{Ashley}@break
   and my blog is located @link["https://example.com"]{here}.

   To reach me directly, send email to ashley@@example.com'''
   env = create_document_env()
   document = Document(run_simple_paxter(input_text, env))

.. code-block:: pycon

   >>> print(document.html())
   <p>Hi, my name is <b>Ashley</b><br />
   and my blog is located <a href="https://example.com">here</a>.</p><p>To reach me directly, send email to ashley@example.com</p>

Of course, the behavior of symbolic replacements can be fully customized
by modifying the content of ``env['_symbols_']`` dictionary to suit your needs.


Stop repeating yourself: document shortcut
------------------------------------------

By the way, the following python code seems to be a recurring pattern.

.. code-block:: python

   from paxter.authoring import create_document_env, run_simple_paxter
   from paxter.authoring.document import Document

   input_text = ...
   env = create_document_env()
   document = Document(run_simple_paxter(input_text, env))

We will use the following shortcut to achieve identical results from now on.

.. code-block:: python

   from paxter.authoring import run_document_paxter

   input_text = ...
   document = run_document_paxter(input_text)

----

Define Common Constants
=======================

Have you ever found yourself repeat yourself *over and over again*?
Writing the same phrase *over and over again* will be a thing of the past.
Imagine a world where you can define a constant once
and reuse it *over and over again*.
You can do so in Paxter in a few different ways.


First method: prepare in advance
--------------------------------

You can prepare the initial python evaluation environment
to also include information about additional aliases.
Remember the dictionary created by
:func:`create_document_env <paxter.authoring.environ.create_document_env>`?
In fact, the content of this dictionary can be customized
by providing additional mapping data through its input arguments.
Then supply the prepared dictionary as the second optional argument
of the function :func:`run_document_paxter <paxter.authoring.preset.run_document_paxter>`.

.. code-block:: python

   from paxter.authoring import create_document_env, run_document_paxter

   customized_env = create_document_env({
       'yaa': "Yet Another Acronym",
   })
   input_text = '''
   YAA is @yaa and it stands for @yaa.
   '''
   document = run_document_paxter(input_text, customized_env)

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

Another method we are going to demonstrate is to
directly define a new python variable right within the document itself.

Document writers can embed any python code for execution
*right inside the input text*
by wrapping the source code within the ``@python`` command.
However, instead of putting the source code
between a pair of matching curly braces,
replace those curly braces with a pair of quotation marks.
Here is an example.

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

Yes, it might have seemed crazy at first,
but this magic is actually *not* part of the core Paxter library.
In order to unveil this magic trick,
we need to focus on what happened to the evaluation environment
dictionary during the parsing and transformation of the document.

Let us look at the same input text again,
but now we will explicitly create a new environment dictionary
for use in :func:`run_document_paxter <paxter.authoring.preset.run_document_paxter>`.

.. code-block:: python

   from paxter.authoring import create_document_env, run_document_paxter

   input_text = '''
   @python"yaa = 'Yet Another Acronym'"
   YAA is @yaa and it stands for @yaa.
   '''
   env = create_document_env()
   document = run_document_paxter(input_text, env)

.. code-block:: pycon

   >>> env
   {'_starter_eval_': <function paxter.authoring.standards.starter_unsafe_eval(starter: str, env: dict) -> Any>,
    'for': DirectApply(wrapped=<function for_statement at 0x7f53f0bffd30>),
    'if': DirectApply(wrapped=<function if_statement at 0x7f53f0bffe50>),
    'python': DirectApply(wrapped=<function python_unsafe_exec at 0x7f53f03a75e0>),
    ...
    ...
    'yaa': 'Yet Another Acronym'}
   >>> print(document.html())
   <p>YAA is Yet Another Acronym and it stands for Yet Another Acronym.</p>


If we compare the contents of ``env`` before and after the call to
:func:`run_document_paxter <paxter.authoring.preset.run_document_paxter>`,
we will find that a lot of stuff get added into ``env`` during the function call,
including the mapping from ``"yaa"`` to ``"Yet Another Acronym"``.
This happened because the command ``@python`` internally called
:func:`exec` built-in function with ``env`` as the global namespace.


Why main argument has to be quoted?
-----------------------------------

Readers might have asked,
*why do we need to wrap the main argument of a command with a pair of quotation marks instead of the matching curly braces? Is this a separate syntax that I have to remember?*

Not quite.
By using quotation marks instead of curly braces,
we merely modified the parsing behavior of the main argument.
To highlight differences between both parsing modes,
let us look at how the above ``@python`` command got parsed.

Specifically, ``@python"yaa = 'Yet Another Acronym'"``
will be parsed to the following equivalent python code.

.. code-block:: python

   python("yaa = 'Yet Another Acronym")

Here, the main argument is no longer parsed as a list;
it is just a plain string!
This behavior has some quirky implications as well:
it is *impossible* to nest a command within the *quoted* main argument
(which in turn implies that we do no longer need to escape ‘**@**’ characters
like what we have done to email addresses previously).


Another way to escape ‘@’
~~~~~~~~~~~~~~~~~~~~~~~~~

Previously we have learned to used symbolic replacements ``@@``
to escape ‘**@**’ symbol characters in email address.
Here we present another way to achieve similar results.

We are going to use ``@verb`` command
(linked to an identity function called
:func:`verbatim <paxter.authoring.standards.verbatim>`
which will output whatever is given as input as-is)
in conjunction with quoted main argument.

.. code-block:: python

   from paxter.authoring import run_document_paxter

   input_text = '''My email is @verb"ashley@example.com".'''
   document = run_document_paxter(input_text)

.. code-block:: pycon

   >>> print(document.html())
   <p>My email is ashley@example.com.</p>


Escaping quotation marks
~~~~~~~~~~~~~~~~~~~~~~~~

The next burning question:
*how do we escape double quotation marks themselves?*
As already mentioned earlier,
Paxter language does not define character escaping mechanisms in a usual way.
For this particular demand, Paxter has adopted
`Rust’s raw string literal <https://doc.rust-lang.org/reference/tokens.html#raw-string-literals>`_
syntax without the ``r`` prefix:
a quoted main argument may be enclosed with any equal number of hash characters.
For example,

.. code-block:: python

   from paxter.authoring import run_document_paxter

   input_text = '''
   @python##"yaa = "Yet Another Acronym""##
   YAA is @yaa and it stands for @yaa.
   '''
   document = run_document_paxter(input_text)

.. code-block:: pycon

   >>> print(document.html())
   <p>YAA is Yet Another Acronym and it stands for Yet Another Acronym.</p>

In the above example, we appended two hash characters
against each end of the quoted main argument.
Using other numbers of hash characters might also work
as long as that number is at least one.
If hash characters were not used,
it would have resulted in an error since the source code
for python would have been ``yaa =`` which is incomplete.

.. code-block:: pycon

   >>> from paxter.authoring import run_document_paxter
   >>> input_text = '''
   ... @python"yaa = "Yet Another Acronym""
   ... YAA is @yaa and it stands for @yaa.
   ... '''
   >>> document = run_document_paxter(input_text)

.. code-block:: pytb

   Traceback (most recent call last):
     File ".../site-packages/paxter/src/paxter/evaluator/context.py", line 171, in transform_command
       return starter_value.call(self, token)
     File ".../site-packages/paxter/src/paxter/evaluator/wrappers.py", line 47, in call
       return self.wrapped(context, node)
     File ".../site-packages/paxter/src/paxter/authoring/standards.py", line 25, in python_unsafe_exec
       exec(code, context.env)
     File "<string>", line 1
       yaa =
            ^
   SyntaxError: invalid syntax

   The above exception was the direct cause of the following exception:

   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
     File ".../site-packages/paxter/src/paxter/authoring/preset.py", line 33, in run_document_paxter
       evaluate_context = EvaluateContext(input_text, env, parse_context.tree)
     File "<string>", line 6, in __init__
     File ".../site-packages/paxter/src/paxter/evaluator/context.py", line 40, in __post_init__
       self.rendered = self.render()
     File ".../site-packages/paxter/src/paxter/evaluator/context.py", line 43, in render
       return self.transform_fragment_list(self.tree)
     File ".../site-packages/paxter/src/paxter/evaluator/context.py", line 122, in transform_fragment_list
       result = [
     File ".../site-packages/paxter/src/paxter/evaluator/context.py", line 122, in <listcomp>
       result = [
     File ".../site-packages/paxter/src/paxter/evaluator/context.py", line 119, in <genexpr>
       self.transform_fragment(fragment)
     File ".../site-packages/paxter/src/paxter/evaluator/context.py", line 73, in transform_fragment
       return self.transform_command(fragment)
     File ".../site-packages/paxter/src/paxter/evaluator/context.py", line 175, in transform_command
       raise PaxterRenderError(
   paxter.exceptions.PaxterRenderError: paxter apply evaluation error at line 2 col 2



Escaping curly braces
~~~~~~~~~~~~~~~~~~~~~

This hash-enclosing mechanisms actually works with main arguments
written in curly braces mode in addition to quoted mode as well.
For example, ``@foo#{Natural numbers are {0, 1, 2, ...}.}#``
will be parsed roughly to the following python code.

.. code-block:: python

   foo(["Natural numbers are {0, 1, 2, ...}."])

----

More Python Code In Documents
=============================

Custom functions
----------------

Continuing on the same line of reasoning,
we could also define functions within ``@python`` command
and use them immediately within a document.

For example, we will create a function that will repeat
the main argument a few times.

.. code-block:: python

   from paxter.authoring import run_document_paxter

   input_text = '''
   @python##"
   def repeat(main_arg, n=2):
       return n * main_arg
   "##

   @repeat{hey}

   @repeat[3]{@bold{hi}}
   '''
   document = run_document_paxter(input_text)

.. code-block:: pycon

   >>> print(document.html())
   <p>heyhey</p><p><b>hi</b><b>hi</b><b>hi</b></p>


Anonymous expressions
---------------------

What if we wish to evaluate some python expressions
and write their results directly into the document?
Of course, one way to achieve this is to
wrap the expression under a new function
and make a call to it through the command syntax.
However, a better way to achieve this is through **anonymous expressions**.

Consider then following example.

.. code-block:: python

   from paxter.authoring import run_document_paxter

   input_text = '''
   @python##"
   def add_one(x):
       return x + 1
   "##

   The computed result of 7×11×13 is @|7 * 11 * 13|.

   Adding one to 99 yields @|add_one(99)|.
   '''
   document = run_document_paxter(input_text)

.. code-block:: pycon

   >>> print(document.html())
   <p>The computed result of 7×11×13 is 1001.</p><p>Adding one to 99 yields 100.</p>

Rest assured.
The syntax ``@|...|`` is *not* a new syntax in Paxter.
So far, all commands we have encountered in this tutorial
are in the form of ``@identifier``
(consisting of an ‘**@**’ symbol
followed by a valid python identifier name).
In fact, ``@identifier`` is a concise form of ``@|identifier|``,
the full-form version of the command syntax.

The textual content between the pair of bars ``@|...|``, however,
are not limited to just python identifiers;
any valid python expressions
(including ``7 * 11 * 13`` and ``add_one(99)``)
are allowed.
Incidentally, a python identifier by itself is a valid python expression.


Escaping bars
~~~~~~~~~~~~~

Similarly to a pair of curly braces or quotation marks,
a pair of bars can be escaped in a similar way:
with enclosing hash characters.
For example,

.. code-block:: python

   from paxter.authoring import run_document_paxter

   input_text = '''
   The union of odd digits and prime digits is
   @#|{1, 3, 5, 7, 9} | {2, 3, 5, 7}|#.
   '''
   document = run_document_paxter(input_text)

.. code-block:: pycon

   >>> print(document.html())
   <p>The union of odd digits and prime digits is
   {1, 2, 3, 5, 7, 9}.</p>


Call to function with attribute lookup
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This full-form of command syntax also allows you to
make a call to functions obtained through attribute lookup
(such as methods of an instance or functions of an imported module).
For example,

.. code-block:: python

   from paxter.authoring import run_document_paxter

   input_text = '''
   @python##"
   import statistics
   d6_faces = [1, 2, 3, 4, 5, 6]
   "##

   The expected outcome of rolling a D6 is @|statistics.mean|[@d6_faces].
   If we remove the first item from the list (which is @|d6_faces.pop|[0])
   then we are left with @|' '.join|[@map[@str, @d6_faces]].
   '''
   document = run_document_paxter(input_text)

.. code-block:: pycon

   >>> print(document.html())
   <p>The expected outcome of rolling a D6 is 3.5.
   If we remove the first item from the list (which is 1)
   then we are left with 2 3 4 5 6.</p>

Let us elaborate on how each command from above is parsed.

.. code-block:: python

   # Command: @|statistics.mean|[@d6_faces]
   statistics.mean(d6_faces)

   # Command: @|d6_faces.pop|[0]
   d6_faces.pop(0)

   # Command: @|' '.join|[@map[@str, @d6_faces]]
   ' '.join(map(str, d6_faces))

.. important::

   There is another quirk about options of a command we have not yet discussed:
   in order to access to the content of an identifier from python environment,
   we need to refer to it using command syntax.
   Hence, an ‘**@**’ symbol in front of the identifier ``d6_faces``
   from the command ``@|statistics.mean|[@d6_faces]`` is required, etc.


.. todo::

   Next topic: what are allowed inside options of a command?
   And the conclusion.
