Getting Started
===============

Installation
------------

Paxter language package can be installed from PyPI via ``pip`` command
(or any other methods of your choice):

.. code-block:: shell

   $ pip install paxter


Programmatic Usage
------------------

This package is *mainly* intended to be utilized as a library.
To get started, let’s assume that we have a document source text
written using **Paxter language syntax**.

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
(implemented by the class :class:`ParseContext <paxter.core.ParseContext>`)
to transform the source input into an intermediate parsed tree.

.. code-block:: python

   from paxter.core import ParseContext

   parsed_tree = ParseContext(source_text).tree

**Note:** We can see the structure of the parsed tree in full
by printing out its content as shown below (output reformatted for clarify).

.. code-block:: pycon

   >>> parsed_tree
   FragmentList(
       start_pos=0,
       end_pos=236,
       children=[
           Command(
               start_pos=1,
               end_pos=148,
               starter="python",
               starter_enclosing=EnclosingPattern(left="", right=""),
               options=None,
               main_arg=Text(
                   start_pos=10,
                   end_pos=145,
                   inner='\n    from datetime import datetime\n\n    name = "Ashley"\n    year_of_birth = 1987\n    current_age = datetime.now().year - year_of_birth\n',
                   enclosing=EnclosingPattern(left='##"', right='"##'),
               ),
           ),
           Text(
               start_pos=148,
               end_pos=161,
               inner="\\\nMy name is ",
               enclosing=EnclosingPattern(left="", right=""),
           ),
           Command(
               start_pos=162,
               end_pos=166,
               starter="name",
               starter_enclosing=EnclosingPattern(left="", right=""),
               options=None,
               main_arg=None,
           ),
           Text(
               start_pos=166,
               end_pos=189,
               inner=" and my current age is ",
               enclosing=EnclosingPattern(left="", right=""),
           ),
           Command(
               start_pos=190,
               end_pos=201,
               starter="current_age",
               starter_enclosing=EnclosingPattern(left="", right=""),
               options=None,
               main_arg=None,
           ),
           Text(
               start_pos=201,
               end_pos=223,
               inner=".\nMy shop opens Monday",
               enclosing=EnclosingPattern(left="", right=""),
           ),
           SymbolCommand(start_pos=224, end_pos=225, symbol=","),
           Text(
               start_pos=225,
               end_pos=226,
               inner="-",
               enclosing=EnclosingPattern(left="", right=""),
           ),
           SymbolCommand(start_pos=227, end_pos=228, symbol=","),
           Text(
               start_pos=228,
               end_pos=236,
               inner="Friday.\n",
               enclosing=EnclosingPattern(left="", right=""),
           ),
       ],
       enclosing=GlobalEnclosingPattern(),
   )


Notice how the source text above also contains what seems like a Python code.
This has *nothing* to do with Paxter core grammar in any way;
it simply uses the Paxter *command* syntax to *embed* Python code
to which we will give a meaningful interpretation later.

Rendering
~~~~~~~~~

Next step, we use a built-in **renderer**
to transform the intermediate parsed tree into its final output.
It is important to remember that
**the semantics of the documents depends on which renderer we are choosing**.

We will adopt the **Python authoring mode** whose renderer
(implemented by :class:`RenderContext <paxter.pyauthor.RenderContext>`)
is already pre-defined by the Paxter library package
to transform the parsed tree into the desired final form.
One of its very useful features is that it will execute python code
under the ``@python`` command.

.. code-block:: python

   from paxter.pyauthor import RenderContext, create_unsafe_env

   # This dictionary data represents the initial global dict state
   # for the interpretation the document tree in python authoring mode.
   env = create_unsafe_env({
       '_symbols_': {',': '&thinsp;'},
   })

   result = RenderContext(source_text, env, parsed_tree).rendered
   print(result)  # or write to a file, etc.

The above code will output the following.

.. code-block:: text

   My name is Ashley and my current age is 33.
   My shop opens Monday&thinsp;-&thinsp;Friday.

.. note::

   Learn more about :doc:`how to use Python authoring mode <python_authoring_mode_tutorial>`
   and :doc:`how to write custom renderer <custom_renderer_tutorial>`.

Create your own function
~~~~~~~~~~~~~~~~~~~~~~~~

We recommend Paxter library users to by themselves write a utility function
to connect all of the toolchains provided Paxter package.
This is the minimal example of a function to get you started.

.. code-block:: python

   from paxter.core import ParseContext
   from paxter.pyauthor import RenderContext, create_unsafe_env

   def interp(source_text: str) -> str:
       parsed_tree = ParseContext(source_text).tree
       result = RenderContext(source_text, create_unsafe_env(), tree).rendered
       return result


Command-Line Usage
------------------

As a shortcut, Paxter library package also provided some utilities
via command-line program.
To get started, red the help message using the following command:

.. code-block:: bash

   $ paxter --help

To play around with the parser, you may use ``parse`` subcommand with an input.
Suppose that we have the following input file.

.. code-block:: bash

   $ cat intro.paxter
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

Then we can see the intermediate parsed tree using this command:

.. code-block:: bash

   $ paxter parse -i intro.paxter

If we wish to also render the document written in Paxter language
under the Python authoring mode with the default environment,
then use the following command:

.. code-block:: bash

   $ paxter pyauthor -i intro.paxter -o result.txt
   $ cat result.txt
   My name is Ashley and my current age is 33.
   My shop opens Monday&thinsp;-&thinsp;Friday.

However, this command-line option does *not* provide a lot of flexibility.
So we recommend users to dig deeper with a more programmatic usage.
It may require a lot of time and effort to setup the entire toolchain,
but it will definitely pay off in the long run.
