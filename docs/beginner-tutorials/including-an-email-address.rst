##########################
Including an Email Address
##########################

As readers have already noticed that ‘**@**’ symbol has special meaning in Paxter language:
it acts as a switch which turns the subsequent piece of input into a command.
Therefore, if library users wish to include ‘**@**’ string literal as-is
in the final output, an escape of some sort is required.

Except that Paxter language actually does *not* provide
a way to *escape* ‘**@**’ symbols per se.
However, there is a way around this.

But first we are going to introduce *another form* of the command syntax:
it begins with an ‘**@**’ character then followed by another symbol character.
This another character will assume the role of the phrase of a command.
On the downside, this form of the command syntax
*neither* accepts the options (i.e. the ``[...]`` pattern)
*nor* accepts the main argument (i.e. the ``{...}`` pattern).

For example, ``@\`` is the command with the single backslash as its phrase part.
Alternatively, ``@@`` is a valid command and it assumes ``@`` as its phrase.

Before we continue on with this new command syntax,
let us revisit the environment dictionary once again.

.. code-block:: pycon

   >>> from paxter.author import create_document_env
   >>> env = create_document_env()
   >>> env
   {'_phrase_eval_': <function paxter.author.standards.phrase_unsafe_eval(phrase: str, env: dict) -> Any>,
    '_extras_': {},
    '@': '@',
    'for': DirectApply(wrapped=<function for_statement at 0x7f8f7c0e5ca0>),
    'if': DirectApply(wrapped=<function if_statement at 0x7f8f7c0e5dc0>),
    'python': DirectApply(wrapped=<function python_unsafe_exec at 0x7f8f6ec20160>),
    'verb': <function paxter.author.standards.verbatim(text: Any) -> str>,
    'raw': paxter.author.elements.RawElement,
    '\\': RawElement(blob='<br />'),
    'line_break': RawElement(blob='<br />'),
    'hrule': RawElement(blob='<hr />'),
    'nbsp': RawElement(blob='&nbsp;'),
    '%': RawElement(blob='&nbsp;'),
    'hairsp': RawElement(blob='&hairsp;'),
    '.': RawElement(blob='&hairsp;'),
    'thinsp': RawElement(blob='&thinsp;'),
    ',': RawElement(blob='&thinsp;'),
    'paragraph': paxter.author.elements.Paragraph,
    'h1': paxter.author.elements.Heading1,
    'h2': paxter.author.elements.Heading2,
    'h3': paxter.author.elements.Heading3,
    'h4': paxter.author.elements.Heading4,
    'h5': paxter.author.elements.Heading5,
    'h6': paxter.author.elements.Heading6,
    'bold': paxter.author.elements.Bold,
    'italic': paxter.author.elements.Italic,
    'uline': paxter.author.elements.Underline,
    'code': paxter.author.elements.Code,
    'blockquote': paxter.author.elements.Blockquote,
    'link': paxter.author.elements.Link,
    'image': paxter.author.elements.Image,
    'numbered_list': paxter.author.elements.NumberedList,
    'bulleted_list': paxter.author.elements.BulletedList}

Recall that Paxter uses this environment dictionary
as a mapping from aliases to the actual python object.
Amazingly, this also works with phrases like ``\`` and ``@`` as well.
According to this particular environment data,
the command ``@@`` is mapped to the string ``"@"``
whereas the command ``@\`` is mapped to the same content as ``@line_break``.

Let us see this in action.

.. code-block:: python

   from paxter.author import create_document_env, run_simple_paxter
   from paxter.author.elements import Document

   input_text = r'''Hi, my name is @bold{Ashley}@\
   and my blog is located @link["https://example.com"]{here}.

   To reach me directly, send email to ashley@@example.com'''
   env = create_document_env()
   document = Document(run_simple_paxter(input_text, env))

.. code-block:: pycon

   >>> print(document.html())
   <p>Hi, my name is <b>Ashley</b><br />
   and my blog is located <a href="https://example.com">here</a>.</p><p>To reach me directly, send email to ashley@example.com</p>

In summary, the ``@@`` commands effectively *simulates*
the escaping of the ‘**@**’ character.
Actually, there is nothing preventing us from mapping
a different phrase to the same ``"@"`` character output
(such as having ``@at`` map to ``"@"`` string in the environment).
*But isn’t this approach kinda neat?*


Don’t Repeat Yourself: Document Shortcut
========================================

By the way, the following python code seems to be a recurring pattern.

.. code-block:: python

   from paxter.author import create_document_env, run_simple_paxter
   from paxter.author.elements import Document

   input_text = ...
   env = create_document_env()
   document = Document(run_simple_paxter(input_text, env))

We will use the following shortcut to achieve identical results from now on.

.. code-block:: python

   from paxter.author import run_document_paxter

   input_text = ...
   document = run_document_paxter(input_text)
