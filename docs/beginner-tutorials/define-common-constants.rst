#######################
Define Common Constants
#######################

Have you ever found yourself having to keep referring
to the same content in writing *over and over again*?
Some of you reader might see that by reiterating on the same content
*over and over again* can be a good reinforcement technique.
Well for most people, that kind of sentiment only applies as readers.
But as an author who wish to communicate consistently,
for us to keep writing and seeing the exact same stuff *over and over again*
would obviously be a very nauseating experience.

Imaging a world where you can just define a piece of information once
and then conveniently refer to it again in an effortless manner.
Well, you can do just that in Paxter in a few different ways.
Introducing, Programming 101.


First Method: Prepare In Advance
================================

Recall that in Paxter ecosystem,
users can prepare the environment dictionary to be used
when input text is parsed and transformed ino the final document object.
Remember the dictionary created by
:func:`create_document_env <paxter.authoring.environ.create_document_env>`
in earlier tutorial?
In fact, the content of this dictionary can be customized
by providing additional mapping data through its input arguments.
Then we supply the just prepared dictionary
as the second optional argument of the function
:func:`run_document_paxter <paxter.authoring.preset.run_document_paxter>`.

.. code-block:: python

   from paxter.authoring import create_document_env, run_document_paxter

   customized_env = create_document_env({
       'yaa': "Yet Another Acronym",
   })
   input_text = '''
   YAA is @yaa and it stands for @yaa.
   '''
   document = run_document_paxter(input_text, customized_env)

.. code-block:: pycon

   >>> customized_env
   {'_phrase_eval_': <function paxter.authoring.standards.phrase_unsafe_eval(phrase: str, env: dict) -> Any>,
    '_extras_': {},
    '@': '@',
    'for': DirectApply(wrapped=<function for_statement at 0x7f7c60e39ca0>),
    'if': DirectApply(wrapped=<function if_statement at 0x7f7c60e39dc0>),
    'python': DirectApply(wrapped=<function python_unsafe_exec at 0x7f7c5245e160>),
    'verb': <function paxter.authoring.standards.verbatim(text: Any) -> str>,
    'raw': paxter.authoring.document.RawElement,
    '\\': RawElement(blob='<br />'),
    'line_break': RawElement(blob='<br />'),
    'hrule': RawElement(blob='<hr />'),
    'nbsp': RawElement(blob='&nbsp;'),
    '%': RawElement(blob='&nbsp;'),
    'hairsp': RawElement(blob='&hairsp;'),
    '.': RawElement(blob='&hairsp;'),
    'thinsp': RawElement(blob='&thinsp;'),
    ',': RawElement(blob='&thinsp;'),
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
    'bulleted_list': paxter.authoring.document.BulletedList,
    'yaa': 'Yet Another Acronym'}
   >>> print(document.html())
   <p>YAA is Yet Another Acronym and it stands for Yet Another Acronym.</p>

Observe that since there exists a mapping from ``yaa``
to the string ``"Yet Another Acronym"`` inside the environment data
(as shown in the last entry above),
we can refer to such string inside input text through the command ``@yaa``.


Second Method: Inject Python Code
=================================

Another method we are going to demonstrate is to
directly define a new python variable right within the document itself.

Document writers can embed any python code for execution
*right inside the input text*
by wrapping the source code within the ``@python`` command.
However, instead of putting the source code
between a pair of matching curly braces,
replace those curly braces with a pair of quotation marks.
Here is an example.

.. code-block:: python

   from paxter.authoring import run_document_paxter

   input_text = '''
   @python"yaa = 'Yet Another Acronym'"
   YAA is @yaa and it stands for @yaa.
   '''
   document = run_document_paxter(input_text)

.. code-block:: pycon

   >>> print(document.html())
   <p>YAA is Yet Another Acronym and it stands for Yet Another Acronym.</p>

Yes, it might have seemed crazy at first,
but this magic is actually *not* part of the core Paxter library.
In order to unveil this magic trick,
we need to focus on what happened to the evaluation environment
dictionary during the parsing and transformation of the document.

Let us look at the same input text again,
but now we will explicitly create a new environment dictionary
for use in :func:`run_document_paxter <paxter.authoring.preset.run_document_paxter>`.

.. code-block:: python

   from paxter.authoring import create_document_env, run_document_paxter

   input_text = '''
   @python"yaa = 'Yet Another Acronym'"
   YAA is @yaa and it stands for @yaa.
   '''
   env = create_document_env()
   document = run_document_paxter(input_text, env)

.. code-block:: pycon

   >>> env
   {'_starter_eval_': <function paxter.authoring.standards.starter_unsafe_eval(starter: str, env: dict) -> Any>,
    'for': DirectApply(wrapped=<function for_statement at 0x7f53f0bffd30>),
    'if': DirectApply(wrapped=<function if_statement at 0x7f53f0bffe50>),
    'python': DirectApply(wrapped=<function python_unsafe_exec at 0x7f53f03a75e0>),
    ...
    ...
    'yaa': 'Yet Another Acronym'}
   >>> print(document.html())
   <p>YAA is Yet Another Acronym and it stands for Yet Another Acronym.</p>


If we compare the contents of ``env`` before and after the call to
:func:`run_document_paxter <paxter.authoring.preset.run_document_paxter>`,
we will find that a lot of stuff get added into ``env`` during the function call,
including the mapping from ``"yaa"`` to ``"Yet Another Acronym"``.
This happened because the command ``@python`` internally called
:func:`exec` built-in function with ``env`` as the global namespace.


Why Main Argument Has To Be Quoted?
===================================

Readers might have asked,
*why do we need to wrap the main argument of a command with a pair of quotation marks instead of the matching curly braces? Is this a separate syntax that I have to remember?*

Not quite.
By using quotation marks instead of curly braces,
we merely modified the parsing behavior of the main argument.
To highlight differences between both parsing modes,
let us look at how the above ``@python`` command got parsed.

Specifically, ``@python"yaa = 'Yet Another Acronym'"``
will be parsed to the following equivalent python code.

.. code-block:: python

   python("yaa = 'Yet Another Acronym")

Here, the main argument is no longer parsed as a list;
it is just a plain string!
This behavior has some quirky implications as well:
it is *impossible* to nest a command within the *quoted* main argument
(which in turn implies that we do no longer need to escape ‘**@**’ characters
like what we have done to email addresses previously).


Another way to escape ‘@’
-------------------------

Previously we have learned to used the command ``@@``
to escape ‘**@**’ symbol characters in email address.
Here we present another way to achieve similar results.

We are going to use ``@verb`` command
(linked to an identity function called
:func:`verbatim <paxter.authoring.standards.verbatim>`
which will output whatever is given as input as-is)
in conjunction with quoted main argument.

.. code-block:: python

   from paxter.authoring import run_document_paxter

   input_text = '''My email is @verb"ashley@example.com".'''
   document = run_document_paxter(input_text)

.. code-block:: pycon

   >>> print(document.html())
   <p>My email is ashley@example.com.</p>


Escaping quotation marks
------------------------

The next burning question:
*how do we escape double quotation marks themselves?*
As already mentioned earlier,
Paxter language does not define character escaping mechanisms in a usual way.
For this particular demand, Paxter has adopted
`Rust’s raw string literal <https://doc.rust-lang.org/reference/tokens.html#raw-string-literals>`_
syntax without the ``r`` prefix:
a quoted main argument may be enclosed with any equal number of hash characters.
For example,

.. code-block:: python

   from paxter.authoring import run_document_paxter

   input_text = '''
   @python##"yaa = "Yet Another Acronym""##
   YAA is @yaa and it stands for @yaa.
   '''
   document = run_document_paxter(input_text)

.. code-block:: pycon

   >>> print(document.html())
   <p>YAA is Yet Another Acronym and it stands for Yet Another Acronym.</p>

In the above example, we prepended and appended two hash characters
against each corresponding end of the quoted main argument.
Using other numbers of hash characters might also work
as long as that number is at least one.
If hash characters were not used,
it would have resulted in an error since the source code
for python would have been ``yaa =``
which is an incomplete python statement in itself.

.. code-block:: pycon

   >>> from paxter.authoring import run_document_paxter
   >>> input_text = '''
   ... @python"yaa = "Yet Another Acronym""
   ... YAA is @yaa and it stands for @yaa.
   ... '''
   >>> document = run_document_paxter(input_text)

.. code-block:: pytb

   Traceback (most recent call last):
     File ".../site-packages/paxter/src/paxter/evaluator/context.py", line 171, in transform_command
       return starter_value.call(self, token)
     File ".../site-packages/paxter/src/paxter/evaluator/wrappers.py", line 47, in call
       return self.wrapped(context, node)
     File ".../site-packages/paxter/src/paxter/authoring/standards.py", line 25, in python_unsafe_exec
       exec(code, context.env)
     File "<string>", line 1
       yaa =
            ^
   SyntaxError: invalid syntax

   The above exception was the direct cause of the following exception:

   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
     File ".../site-packages/paxter/src/paxter/authoring/preset.py", line 33, in run_document_paxter
       evaluate_context = EvaluateContext(input_text, env, parse_context.tree)
     File "<string>", line 6, in __init__
     File ".../site-packages/paxter/src/paxter/evaluator/context.py", line 40, in __post_init__
       self.rendered = self.render()
     File ".../site-packages/paxter/src/paxter/evaluator/context.py", line 43, in render
       return self.transform_fragment_list(self.tree)
     File ".../site-packages/paxter/src/paxter/evaluator/context.py", line 122, in transform_fragment_list
       result = [
     File ".../site-packages/paxter/src/paxter/evaluator/context.py", line 122, in <listcomp>
       result = [
     File ".../site-packages/paxter/src/paxter/evaluator/context.py", line 119, in <genexpr>
       self.transform_fragment(fragment)
     File ".../site-packages/paxter/src/paxter/evaluator/context.py", line 73, in transform_fragment
       return self.transform_command(fragment)
     File ".../site-packages/paxter/src/paxter/evaluator/context.py", line 175, in transform_command
       raise PaxterRenderError(
   paxter.exceptions.PaxterRenderError: paxter apply evaluation error at line 2 col 2


Escaping curly braces
---------------------

This hash-enclosing mechanisms actually works with main arguments
written in curly braces mode in addition to quoted mode as well.
For example, ``@foo#{Natural numbers are {0, 1, 2, ...}.}#``
will be parsed roughly to the following python code.

.. code-block:: python

   foo(["Natural numbers are {0, 1, 2, ...}."])
