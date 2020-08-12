######################
Add a Second Paragraph
######################

In the previous section,
we have written a blog entry with a single paragraph,
but it was way too short.
So we will add another one.

.. code-block:: python

   from paxter.authoring import create_document_env, run_simple_paxter

   input_text = '''@paragraph{Hi, my name is @bold{Ashley}@line_break
   and my blog is located @link["https://example.com"]{here}.}

   @paragraph{This is another paragraph.}'''
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
       ),
       "\n\n",
       Paragraph(blob=Fragments(["This is another paragraph."])),
   ])

The resulting ``document`` (shown above)
is a :class:`Fragments <paxter.evaluator.data.Fragments>` list of
:class:`str` or :class:`Element <paxter.authoring.document.Element>` instances
(from which :class:`Paragraph <paxter.authoring.document.Paragraph>` is derived).
Unfortunately, the :class:`Fragments <paxter.evaluator.data.Fragments>` class
does not provide a method to render itself into a final output *by design*
as it is merely part of the result of parsing and evaluate
input text in Paxter language.
We need another utility from the :mod:`paxter.authoring` domain
to help us render it.


Document Helper Class
=====================

Paxter’s authoring subpackage provides a data class called
:class:`Document <paxter.authoring.document.Document>`
to wrap over the object returned by
:func:`run_simple_paxter <paxter.authoring.preset.run_simple_paxter>`.
Then we call the :meth:`html() <paxter.authoring.document.Element>` method
to render the HTML output.

.. code-block:: python

   from paxter.authoring import create_document_env, run_simple_paxter
   from paxter.authoring.document import Document

   input_text = '''@paragraph{Hi, my name is @bold{Ashley}@line_break
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

   input_text = '''Hi, my name is @bold{Ashley}@line_break
   and my blog is located @link["https://example.com"]{here}.

   This is another paragraph.

   @bold{This is a third paragraph.}'''
   env = create_document_env()
   document = Document(run_simple_paxter(input_text, env))

.. code-block:: pycon

   >>> document
   Document(
       blob=Fragments([
           Paragraph(
               blob=Fragments([
                   "Hi, my name is ",
                   Bold(blob=Fragments(["Ashley"])),
                   RawElement(blob="<br />"),
                   "\nand my blog is located ",
                   Link(blob=Fragments(["here"]), href="https://example.com"),
                   ".",
               ])
           ),
           Paragraph(blob=Fragments(["This is another paragraph."])),
           Bold(blob=Fragments(["This is a third paragraph."])),
       ])
   )
   >>> print(document.html())
   <p>Hi, my name is <b>Ashley</b><br />
   and my blog is located <a href="https://example.com">here</a>.</p><p>This is another paragraph.</p><b>This is a third paragraph.</b>

Watch out for the third paragraph above!
They are surrounded by ``<b>`` tag in the result,
but the enclosing ``<p>`` tag is missing.
In this case, the explicit ``@paragraph`` marking is required.

.. code-block:: python

   input_text = '''Hi, my name is @bold{Ashley}@line_break
   and my blog is located @link["https://example.com"]{here}.

   This is another paragraph.

   @paragraph{@bold{This is a third paragraph.}}'''
   env = create_document_env()
   document = Document(run_simple_paxter(input_text, env))

.. code-block:: pycon

   >>> print(document.html())
   <p>Hi, my name is <b>Ashley</b><br />
   and my blog is located <a href="https://example.com">here</a>.</p><p>This is another paragraph.</p><p><b>This is a third paragraph.</b></p>
