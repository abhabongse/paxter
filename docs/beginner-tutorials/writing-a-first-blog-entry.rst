##########################
Writing a First Blog Entry
##########################

Let us write a simple blog entry.
Consider the following python code in which
``paragraph`` object is constructed using data classes
from :mod:`paxter.authoring.document` subpackage
(please ignore the usage of
:class:`Fragments <paxter.evaluator.data.Fragments>` class for now).

.. code-block:: python

   from paxter.authoring.document import Bold, Link, Paragraph, line_break
   from paxter.evaluator.data import Fragments

   paragraph = Paragraph(
       Fragments([
           "Hi, my name is ",
           Bold(Fragments(["Ashley"])),
           line_break,
           "\nand my blog is located ",
           Link(Fragments(["here"]), "https://example.com"),
           ".",
       ])
   )

.. important::

   Everything located under the subpackage :mod:`paxter.authoring`
   are supplementary to but independent of the core Paxter library package.
   They are provided only for convenience.

Then we call the method :meth:`html() <paxter.authoring.document.Element.html>`
on the ``paragraph`` object in order to render
its content into the final HTML string.

.. code-block:: pycon

   >>> print(paragraph.html())
   <p>Hi, my name is <b>Ashley</b><br />
   and my blog is located <a href="https://example.com">here</a>.</p>

Of course, this way of authoring a document
right inside the python code space is extremely inconvenient.
Therefore, we are going to approach this differently,
using another tool provided by Paxter library
to construct the exact same document.

.. code-block:: python

   from paxter.authoring import create_document_env, run_simple_paxter

   # The following input text is written in-code for a simpler example.
   # However in reality, input text may be read from other sources
   # such as text files, some databases, or even fetched via some API.

   input_text = '''@paragraph{Hi, my name is @bold{Ashley}@line_break
   and my blog is located @link["https://example.com"]{here}.}'''
   env = create_document_env()
   document = run_simple_paxter(input_text, env)

.. code-block:: pycon

   >>> document
   Fragments([
       Paragraph(
           blob=Fragments([
               "Hi, my name is ",
               Bold(blob=Fragments(["Ashley"])),
               RawElement(blob="<br />"),
               "\nand my blog is located ",
               Link(blob=Fragments(["here"]), href="https://example.com"),
               ".",
           ])
       )
   ])
   >>> document[0] == paragraph  # paragraph from the previous example
   True
   >>> print(document[0].html())
   <p>Hi, my name is <b>Ashley</b><br />
   and my blog is located <a href="https://example.com">here</a>.</p>

The above example demonstrates one important point about Paxter library,
which is that we can author a document through
an intuitive language (called the Paxter language)
and then we use Paxter library package to help us
parse and transform the input text into the final document object.
Paxter is designed to be flexible and very customizable
to help us achieve the desired output document.

Next we are going to walk though a few concepts
that we have seen in the input text from the example above.


Understanding Commands
======================

.. code-block:: paxter

   @paragraph{Hi, my name is @bold{Ashley}@line_break
   and my blog is located @link["https://example.com"]{here}.}

Let us look inside the content of ``input_text`` from the previous example.
Notice the common pattern among
``@line_break``, ``@paragraph{...}``, ``@bold{..}``, and ``@link[...]{...}``.
They are known as **commands** in Paxter language.

Each command always begins with an ‘**@**’ symbol
and is immediately followed by what is called a **phrase**
(e.g. the ``line_break``, ``paragraph``, ``bold``, and ``link`` part)
Then it may be *optionally* be followed by the ``[...]`` pattern
or the ``{...}`` pattern (or both, in this order).
When at least one of the optional part is present,
the command would simulate a function call.

For example, ``@line_break`` simply refers to an object
which is stored within the identifier ``line_break``.
On the other hand, ``@bold{Ashley}`` from the Paxter input text
resembles a function call to ``bold`` with a parameter ``Ashley``.
In particular, it is roughly equivalent to this python code:

.. code-block:: python

   bold(Fragments(["Ashley"]))

which would be evaluated into the following.

.. code-block:: python

   Bold(blob=Fragments(["Ashley"]))

Similarly, ``@link["https://example.com"]{here}`` from inside the input text
would roughly be parsed into the following python code

.. code-block:: python

   link(Fragments(["here"]), "https://example.com")

which in turn, would be evaluated into

.. code-block:: python

   Link(blob=Fragments(['here']), href='https://example.com')

Pay attention of how the ``{...}`` part of the command
is parsed into the python code.
Firstly, notice that the textual content
that is surrounded by *a matching pair of curly braces*
are always parsed into an instance of
:class:`Fragments <paxter.evaluator.data.Fragments>`,
containing a list of values.
And secondly, it would always be positioned
as the very first argument of the translated function call.
We call this part the **main argument** of a command.

Moreover, if we look at how the outermost ``@paragraph{...}`` command is constructed,
we would see that the content of main argument
would always be *recursively parsed* into
a :class:`Fragments <paxter.evaluator.data.Fragments>` instance with nested values.
Hence, the ``@paragraph`` command from above is in fact
roughly parsed into an equivalent python code as follows.

.. code-block:: python

   paragraph(
       Fragments([
           "Hi, my name is ",
           bold(Fragments(["Ashley"])),
           break_,
           "\nand my blog is located ",
           link(Fragments(["here"]), "https://example.com"),
           ".",
       ]),
   )

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

   foo(Fragments(["main argument"]), "bar", 3)

Python-style keyword arguments are also supported within the options.
For instance, the Paxter command ``@foo["bar", n=3]{main argument}`` gets turned into:

.. code-block:: python

   foo(Fragments(["main argument"]), "bar", n=3)

In addition, the main argument discussed earlier is actually *not* mandatory.
When it is absent, all values within the options then
become sole arguments of the function call.
Therefore, the command ``@foo["bar", n=3]`` would simply be parsed into

.. code-block:: python

   foo("bar", n=3)

As a special case, to make a function call with zero arguments from a command,
simply write a pair of square brackets without anything inside it
(e.g. ``@foo[]``).

To recap, a Paxter command consists of three parts:
the phrase, the options, and the main argument,
the last two of which are *optional*.

.. important::

   Finally, do take note that the main argument and the options of a command
   only try to mimic function call patterns in python;
   it actually does *not* fully support python syntax inside it.
   The full description of what is supported by Paxter language
   :doc:`will be discussed later <making-a-list-of-items>`.


Understanding Environments
==========================

At this point, please note that ``@paragraph``, ``@bold``, and ``@link``
are merely aliases to the constructors of actual data classes
:class:`Paragraph <paxter.authoring.document.Paragraph>`,
:class:`Bold <paxter.authoring.document.Bold>`,
and :class:`Link <paxter.authoring.document.Link>` respectively.
These relationships are evident once we inspect
the content of the environment dictionary ``env`` (shown below).
Additionally, note that ``@break`` simply maps to the value
``RawElement(children='<br />')``.

.. code-block:: pycon

   >>> env
   {'_phrase_eval_': <function paxter.authoring.standards.phrase_unsafe_eval(phrase: str, env: dict) -> Any>,
    '_extras_': {},
    '@': '@',
    'for': DirectApply(wrapped=<function for_statement at 0x7f34d0660e50>),
    'if': DirectApply(wrapped=<function if_statement at 0x7f34d0660c10>),
    'python': DirectApply(wrapped=<function python_unsafe_exec at 0x7f34c1b2a1f0>),
    'verb': <function paxter.authoring.standards.verbatim(text: Any) -> str>,
    'raw': paxter.authoring.document.RawElement,
    '\\': RawElement(blob='<br />'),
    'line_break': RawElement(blob='<br />'),
    'hrule': RawElement(blob='<hr />'),
    'nbsp': RawElement(blob='&nbsp;'),
    '%': RawElement(blob='&nbsp;'),
    'hairsp': RawElement(blob='&hairsp;'),
    '.': RawElement(blob='&hairsp;'),
    'thinsp': RawElement(blob='&thinsp;'),
    ',': RawElement(blob='&thinsp;'),
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
       # _phrase_eval_ is required, but ignore this part for now
       '_phrase_eval_': standards.phrase_unsafe_eval,
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
