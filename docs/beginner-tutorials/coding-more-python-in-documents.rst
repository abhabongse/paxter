###############################
Coding More Python In Documents
###############################

Custom Functions
================

Continuing on the same line of reasoning,
we could also define functions within ``@python`` command
and use them immediately within a document.

For example, we will create a function that will repeat
the main argument a few times.

.. code-block:: python

   from paxter.author import run_document_paxter

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
wrap the expression under a new python function
and make a call to it through the command syntax.
However, a better way to achieve this is through **anonymous expressions**.

Consider then following example.

.. code-block:: python

   from paxter.author import run_document_paxter

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

Rest assured; the syntax of the form ``@|...|``
is *not* a whole new syntax we have not yet introduced.
Previously, we have already seen the other two patterns of a command,
which are:

- **First form:** a command of the form ``@identifier``
  (including ``@identifier[...]``, ``@identifier{...}``,
  and ``@identifier[...]{...}``).
  It begins with an ‘**@**’ symbol followed by a phrase
  in the valid python identifier form.

- **Second form:** a command which consists of an ‘**@**’ symbol
  followed by another symbol character.

In fact, this new form of the command syntax ``@|...|``
is actually the *expanded* version (or the *full-form* version)
of the first form described above.
Specifically, the phrase ``@identifier``
is just the concise version of ``@|identifier|``
(and the command ``@identifier[...]{...}`` is also
the concise version of ``@|identifier|[...]{...}``
respectively, etc.).

The textual content between a pair of bars in ``@|...|``
is indeed the phrase of the command,
but it does not necessarily have to be a valid a python identifier;
it can be just anything,
including ``@|7 * 11 * 13|`` and ``@|add_one(99)|``
that we have seen in the above example.
Note that one can also say that ``@|%|`` and ``@|@|``
are the full-form version of ``@%`` and ``@@`` commands as well.

Recall that the phrase part of a command has been used
as a dictionary lookup key for the mapped values
inside the pre-defined environment.
What we have not yet discussed is that,
if the dictionary lookup was failed,
then the fallback step is to evaluate the entire phrase of the command
using python built-in function :func:`eval`
with the environment dictionary as the global namespace
to obtain the final result.
Therefore, ``@|7 * 11 * 13|`` is evaluated to ``1001`` in python
and this result is then transferred to the final document output.
The same principle applies to ``@|add_one(99)|`` as well.

.. important::

   The specific evaluation behavior of the phrase of a command
   is actually *not* part of the core Paxter library package.
   It is controlled by the function
   :func:`phrase_unsafe_eval <paxter.author.standards.phrase_unsafe_eval>`
   which is stored under the item ``_phrase_eval_`` of the environment dictionary.

   This explains why we need to provide this mapping information
   when we customize the environment dictionary ``alternative_env`` in
   :ref:`an earlier tutorial <beginner-tutorials/writing-a-first-blog-entry:Understanding Environments>`?

   Users of Paxter library package can fully customize the phrase evaluation behavior
   by providing their own function to the ``_phrase_eval_`` item of the environment.
   They are encouraged to read the source code of
   :func:`phrase_unsafe_eval <paxter.author.standards.phrase_unsafe_eval>`
   to obtain some inspirations.


Escaping bars
-------------

Similarly to a pair of curly braces or quotation marks for the main argument,
a pair of bars can be escaped in a similar way:
with enclosing hash characters.
For example,

.. code-block:: python

   from paxter.author import run_document_paxter

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

   from paxter.author import run_document_paxter

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
   The next page will discuss this in further details.
