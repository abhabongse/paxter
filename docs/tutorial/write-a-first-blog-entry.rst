########################
Write a First Blog Entry
########################

While not required, Paxter package provides a set of data classes
that users can use to construct a rich document.
Here suppose that we are going to write a simple blog entry
using a few data classes from :mod:`paxter.authoring` subpackage.
Please ignore :class:`Fragments <paxter.evaluator.Fragments>` for now.

.. code-block:: python

   from paxter.authoring.document import Bold, Link, Paragraph, line_break
   from paxter.evaluator import Fragments

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

.. code-block:: pycon

   >>> print(paragraph.html())
   <p>Hi, my name is <b>Ashley</b><br />
   and my blog is located <a href="https://example.com">here</a>.</p>

.. important::

   Everything located under the subpackage :mod:`paxter.authoring`
   are supplementary to but independent of the core Paxter library package.
   They are provided only for convenience.

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

An important point demonstrated in the above example is that
we write a document through an intuitive language
and then use Paxter library package to help us and parse and transform
the input text we wrote into the final document object.
Paxter library is designed to be flexible and customizable
to help us achieve the desired output document.

Next we are going to walk though a few concepts
we have seen in the input text from the above example.


Understanding Commands
======================

Parts that begin with an ‘**@**’ symbol in Paxter input text
(e.g. ``@paragraph``, ``@bold``, ``@break``, and ``@link``)
are known as **commands** in Paxter language.
Commands can either be in the standalone form (like how ``@break`` appears)
or, when followed by at least one of ``[options]`` or ``{main argument}``,
it simulates a function call over such object.

For example, ``@bold{Ashley}`` in Paxter input text
is roughly equivalent to the python code ``bold(Fragments(["Ashley"]))``
which would be evaluated into ``Bold(blob=Fragments(["Ashley"]))`` in the final result.
Similarly,

.. code-block:: paxter

   @link["https://example.com"]{here}

would roughly be parsed into the following python code

.. code-block:: python

   link(Fragments(["here"]), "https://example.com")

which would then be evaluated into

.. code-block:: python

   Link(blob=Fragments(['here']), href='https://example.com')

Notice that the textual content
that is surrounded by *a matching pair of curly braces*
is always parsed into an instance of
:class:`Fragments <paxter.evaluator.Fragments>`,
containing a list of values.
Moreover, it would always be positioned
as the very first argument of translated function calls.
We call this part the **main argument** of a command.

Moreover, if we look at how the outermost ``@paragraph`` command is constructed,
we would see that the content of main argument
would always be *recursively parsed* into
a :class:`Fragments <paxter.evaluator.Fragments>` instance with nested values.
Hence, the above particular ``@paragraph`` command is in fact
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

.. important::

   Finally, do take note that the main argument and the options of a command
   only try to mimic function call patterns in python;
   it actually does *not* fully support python syntax inside it.
   The full description of what is supported by Paxter language
   is discussed in :doc:`Paxter Language Tutorial <../paxter_language_tutorial>` page.


Understanding Environments
==========================

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
