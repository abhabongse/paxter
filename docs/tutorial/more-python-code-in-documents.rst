#############################
More Python Code In Documents
#############################

Custom Functions
================

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


Anonymous Expressions
=====================

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
-------------

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
--------------------------------------

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
