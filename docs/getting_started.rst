Getting Started
===============

Installation
------------

Paxter language package can be installed from PyPI via ``pip`` command (or any other methods of your choice):

.. code-block:: shell

   $ pip install paxter


Programmatic Usage
------------------

The package is *mainly* intended to be used as a library.
To get started, let’s assume that we have a source text
which contains a document **written in Paxter language syntax**.

.. code-block:: python

   # Of course, input text of a document may be read from any source,
   # such as from a text file loaded from the filesystem, from user input, etc.

   source_text = """\
   @python##"
       from datetime import datetime

       name = "Ashley"
       year_of_birth = 1987
       current_age = datetime.now().year - year_of_birth
   "##\\
   My name is @name and my current age is @current_age.
   My shop opens Monday@,-@,Friday.
   """

.. note::

   Learn more about :doc:`Paxter language grammar and features <tutorials>`.

Parsing
~~~~~~~

First and foremost, we use a **parser**
(which is implemented by the class :class:`ParseContext <paxter.core.ParseContext>`)
to transform the source text into a parsed document tree.

.. code-block:: python

   from paxter.core import ParseContext

   tree = ParseContext(source_text).parse()

**Note:** We can see the structure of the document tree in full by printing out
the content of the variable ``tree`` from above (output reformatted for clarity).

.. code-block:: pycon

   >>> tree
   FragmentList(
       children=[
           PaxterApply(
               id=Identifier(name="python"),
               options=None,
               main_arg=Text(
                   inner='\n    from datetime import datetime\n\n    name = "Ashley"\n    year_of_birth = 1987\n    current_age = datetime.now().year - year_of_birth\n',
                   scope_pattern=ScopePattern(opening='##"', closing='"##'),
                   is_command=False,
               ),
           ),
           Text(
               inner="\nMy name is ",
               scope_pattern=ScopePattern(opening="", closing=""),
               is_command=False,
           ),
           PaxterPhrase(inner="name", scope_pattern=ScopePattern(opening="", closing="")),
           Text(
               inner=" and my current age is ",
               scope_pattern=ScopePattern(opening="", closing=""),
               is_command=False,
           ),
           PaxterPhrase(
               inner="current_age", scope_pattern=ScopePattern(opening="", closing="")
           ),
           Text(
               inner=".\nMy shop opens Monday",
               scope_pattern=ScopePattern(opening="", closing=""),
               is_command=False,
           ),
           PaxterPhrase(inner=",", scope_pattern=ScopePattern(opening="", closing="")),
           Text(
               inner="-",
               scope_pattern=ScopePattern(opening="", closing=""),
               is_command=False,
           ),
           PaxterPhrase(inner=",", scope_pattern=ScopePattern(opening="", closing="")),
           Text(
               inner="Friday.\n",
               scope_pattern=ScopePattern(opening="", closing=""),
               is_command=False,
           ),
       ],
       scope_pattern=GlobalScopePattern(opening="", closing=""),
       is_command=False,
   )


Notice that the source text above also contains what seems like a python code.
This is **not** part of the Paxter language grammar in any way;
it simply uses the Paxter application command to embed python code,
to which we will give meaningful interpretation later.

Rendering
~~~~~~~~~

Next step, we use a **renderer** to transform the document tree into its final output.
It is important to remember that
**the semantics of the document is given depending on which renderer we choose**.

We will use :class:`paxter.renderers.python.RenderContext`
already pre-defined by Paxter library package
to render the document tree into the final output.
One of its useful features is that it will execute python code
wrapped by ``@python`` application command.

.. code-block:: python

   from paxter.renderers.python import RenderContext, create_unsafe_env

   # This dictionary data represents the initial global dict state
   # for the interpretation the document tree in python authoring mode.
   env = create_unsafe_env({
       '_symbols_': {',': '&thinsp;'},
   })

   output_text = RenderContext(source_text, env, tree).render()
   print(output_text)  # or write to a file, etc.

The above code will output the following.

.. code-block:: text

   My name is Ashley and my current age is 33.
   My shop opens Monday&thinsp;-&thinsp;Friday.

.. note::

   Learn more about :doc:`how to use Python authoring mode <tutorials>`
   and :doc:`how to write custom renderer <tutorials>`.

Create Your Function
~~~~~~~~~~~~~~~~~~~~

In order to reuse this parse-and-render setup,
we can write a utility function such as in the following:

.. code-block:: python

   from paxter.core import ParseContext
   from paxter.renderers.python import RenderContext, create_unsafe_env

   def interp(source_text: str) -> str:
       tree = ParseContext(source_text).parse()
       output = RenderContext(source_text, create_unsafe_env(), tree).render()
       return output

Command-Line Usage
------------------

As a shortcut, Paxter library package also provides utility via command-line.
To get started, read the help message by typing:

.. code-block:: bash

   $ paxter --help

To get the parsing result only, we will use ``parse`` subcommand.
Suppose that we have an input file called ``intro.paxter`` which contains
the following text:

.. code-block:: text

   @python##"
       from datetime import datetime

       _symbols_ = {
           ',': '&thinsp;',
       }
       name = "Ashley"
       year_of_birth = 1987
       current_age = datetime.now().year - year_of_birth
   "##\
   My name is @name and my current age is @current_age.
   My shop opens Monday@,-@,Friday.

Then we can look at the intermediate parsed tree result with the following command:

.. code-block:: bash

   $ paxter parse -i intro.paxter

If we wish to render the document source text with the default environment dict,
then we can use the following command:

.. code-block:: bash

   $ paxter python-authoring -i intro.paxter

which will result in

.. code-block:: text

   My name is Ashley and my current age is 33.
   My shop opens Monday&thinsp;-&thinsp;Friday.
