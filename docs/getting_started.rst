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

   Learn more about :doc:`Paxter language grammar and features <paxter_language_tutorial>`.

Parsing
~~~~~~~

First and foremost, we use a **parser**
(which is implemented by the class :class:`ParseContext <paxter.core.ParseContext>`)
to transform the source text into a parsed document tree.

.. code-block:: python

   from paxter.core import ParseContext

   tree = ParseContext(source_text).tree

**Note:** We can see the structure of the document tree in full by printing out
the content of the variable ``tree`` from above (output reformatted for clarity).

.. code-block:: pycon

   >>> tree
   FragmentList(
       start_pos=0,
       end_pos=236,
       children=[
           Command(
               start_pos=1,
               end_pos=148,
               intro="python",
               intro_enclosing=EnclosingPattern(left="", right=""),
               options=None,
               main_arg=Text(
                   start_pos=10,
                   end_pos=145,
                   inner='\n    from datetime import datetime\n\n    name = "Ashley"\n    year_of_birth = 1987\n    current_age = datetime.now().year - year_of_birth\n',
                   enclosing=EnclosingPattern(left='##"', right='"##'),
                   at_prefix=False,
               ),
           ),
           Text(
               start_pos=148,
               end_pos=161,
               inner="\\\nMy name is ",
               enclosing=EnclosingPattern(left="", right=""),
               at_prefix=False,
           ),
           Command(
               start_pos=162,
               end_pos=166,
               intro="name",
               intro_enclosing=EnclosingPattern(left="", right=""),
               options=None,
               main_arg=None,
           ),
           Text(
               start_pos=166,
               end_pos=189,
               inner=" and my current age is ",
               enclosing=EnclosingPattern(left="", right=""),
               at_prefix=False,
           ),
           Command(
               start_pos=190,
               end_pos=201,
               intro="current_age",
               intro_enclosing=EnclosingPattern(left="", right=""),
               options=None,
               main_arg=None,
           ),
           Text(
               start_pos=201,
               end_pos=223,
               inner=".\nMy shop opens Monday",
               enclosing=EnclosingPattern(left="", right=""),
               at_prefix=False,
           ),
           Command(
               start_pos=224,
               end_pos=225,
               intro=",",
               intro_enclosing=EnclosingPattern(left="", right=""),
               options=None,
               main_arg=None,
           ),
           Text(
               start_pos=225,
               end_pos=226,
               inner="-",
               enclosing=EnclosingPattern(left="", right=""),
               at_prefix=False,
           ),
           Command(
               start_pos=227,
               end_pos=228,
               intro=",",
               intro_enclosing=EnclosingPattern(left="", right=""),
               options=None,
               main_arg=None,
           ),
           Text(
               start_pos=228,
               end_pos=236,
               inner="Friday.\n",
               enclosing=EnclosingPattern(left="", right=""),
               at_prefix=False,
           ),
       ],
       enclosing=GlobalEnclosingPattern(),
       at_prefix=False,
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

   output_text = RenderContext(source_text, env, tree).rendered
   print(output_text)  # or write to a file, etc.

The above code will output the following.

.. code-block:: text

   My name is Ashley and my current age is 33.
   My shop opens Monday&thinsp;-&thinsp;Friday.

.. note::

   Learn more about :doc:`how to use Python authoring mode <python_authoring_mode_tutorial>`
   and :doc:`how to write custom renderer <custom_renderer_tutorial>`.

Create Your Function
~~~~~~~~~~~~~~~~~~~~

In order to reuse this parse-and-render setup,
we can write a utility function such as in the following:

.. code-block:: python

   from paxter.core import ParseContext
   from paxter.renderers.python import RenderContext, create_unsafe_env

   def interp(source_text: str) -> str:
       tree = ParseContext(source_text).tree
       output = RenderContext(source_text, create_unsafe_env(), tree).rendered
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
