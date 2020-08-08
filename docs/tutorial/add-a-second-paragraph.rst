######################
Add a Second Paragraph
######################

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


Document Helper Class
=====================

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
