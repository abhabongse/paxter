########################
Include an Email Address
########################

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


Don’t Repeat Yourself: Document Shortcut
========================================

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
