##############
Quick Blogging
##############

To get started with blogging or writing an article,
we will learn how to write something using Paxter language syntax
and then how to use the Paxter package toolchain
to convert it into HTML output.

.. important::

   Many of the following descriptions of Paxter language
   are *actually not* tied to the core Paxter language at all.
   Paxter library (which includes the core Paxter language)
   is designed to be fully extensible and customizable.
   The following descriptions of Paxter language
   are merely one possibly configuration
   pre-defined by the Paxter package library.


Bolds, Italics, and Underline
=============================

We begin with one of the most basic form of **a command**
(to be discussed in finer details in later sections).
To bold part of a text, we use the command ``@bold{...}`` ,
replacing ``...`` with part of the text to be emphasized.

For example, consider the following text written in Paxter language.

.. code-block:: paxter

   Here is how to @bold{bold the text}.

If we saved the above content into a file called ``"input.paxter"``,
we can render the HTML output using the following shell command
(assuming that Paxter package library is already installed):

.. code-block:: bash

   $ paxter html -i input.paxter

and we will get the following HTML output

.. code-block:: html

   <p>Here is how to <b>bold the text</b>.</p>

which will then be displayed as follows.

.. raw:: html

   <blockquote><p>Here is how to <b>bold the text</b>.</p></blockquote>

Likewise, for italicized text and underlined text,
use the command ``@italic{...}`` and ``@uline{...}`` respectively.

Please note that these commands can also be nested.
For example,

.. code-block:: paxter

   This is @italic{so important that @uline{multiple emphasis} is required}.

When the above example gets rendered into HTML,
we get the following output.

.. code-block:: html

   <p>This is <i>so important that <u>multiple emphasis</u> is required</i>.</p>

which will be displayed as

.. raw:: html

   <blockquote><p>This is <i>so important that <u>multiple emphasis</u> is required</i>.</p></blockquote>


Monospaced Code
===============

Similarly to text emphases with bold, italic, and underline,
we use the command ``@code{...}`` to encapsulate text
to be displayed as monospaced code.

For example, this text written in Paxter language

.. code-block:: paxter

   Run the @code{python} command.

will be evaluated into the HTML output shown below.

.. code-block:: html

   <p>Run the <code>python</code> command.</p>


Multiple Paragraphs
===================

To author multiple paragraphs,
simply put at least two newline characters between chunks of text.
Consider the following example containing three paragraphs.

.. code-block:: paxter

   This is @bold{the first paragraph}.
   This is the second sentence of the first paragraph.

   This is @italic{another} paragraph.

   This is the @uline{final} paragraph.

The above text in Paxter language will be transformed
into the following HTML.

.. code-block:: html

   <p>This is <b>the first paragraph</b>.
      This is the second sentence of the first paragraph.</p>
   <p>This is <i>another</i> paragraph.</p>
   <p>This is the <u>final</u> paragraph.</p>


Headings
========

To include a heading (from level 1 to level 6)
use the command ``@h1{...}`` through ``@h6{...}`` on its own chunk.
They must be separated from other chunks with at least two newline characters
just like a paragraph.

.. code-block:: paxter

   @h1{New Blog!}

   @bold{Welcome to the new blog!} Let’s celebrate!

   @h2{Updates}

   There is no update.

.. code-block:: html

   <h1>New Blog!</h1>
   <p><b>Welcome to the new blog!</b> Let’s celebrate!</p>
   <h2>Updates</h2>
   <p>There is no update.</p>

Observe that the ``@h1{...}`` and ``@h2{...}`` were *not* used
to encapsulate the heading text,
they would have been rendered as its own paragraph.
Try that for yourself.

Also, what happens if the command did not surround the entire text?
Let’s look at this example
(notice that the exclamation mark is *outside* the command):

.. code-block:: paxter

   @h1{New Blog}!

   @bold{Welcome to the new blog!} Let’s celebrate!

.. code-block:: html

   <p><h1>New Blog</h1>!</p>
   <p><b>Welcome to the new blog!</b> Let’s celebrate!</p>

Since *not* the entire chunk of heading text
is encapsulated by the ``@h1{...}`` command,
Paxter assumes that it is simply just a paragraph.
So beware of this kind of errors.


Blockquote
==========

The ``@blockquote{...}`` command must reside on its own chunk just like a heading.
So the following Paxter input text

.. code-block:: paxter

   They said that

   @blockquote{I refuse.}

would be transformed into the following HTML output.

.. code-block:: html

   <p>They said that</p>
   <blockquote>I refuse.</blockquote>

However, suppose that we want to include multiple paragraphs inside the blockquote.
We can follow the similar rules to how to write multiple paragraphs:
by separating them with at least two newline characters.

Hence, the following Paxter text input

.. code-block:: paxter

   They said that

   @blockquote{
       I refuse.

       Then I regret.
   }

will be rendered into the following HTML.

.. code-block:: html

   <p>They said that</p>
   <blockquote>
       <p>I refuse.</p>
       <p>Then I regret.</p>
   </blockquote>

The important key to note here is that,
each paragraph within the blockquote will be surrounded by
a paragraph tag ``<p>...</p>``
*unless only one paragraph exists*.

The above behavioral rule is enforced mainly for convenience.
However, if we wish to force wrap the only paragraph within the blockquote
with a paragraph tag,
we can manually wrap that part of text with the ``@paragraph{...}`` command.

Considering the first example of this section again.
If we wish to have a paragraph tag surround “I refuse.”
then we can write as follows.

.. code-block:: paxter

   They said that

   @blockquote{@paragraph{I refuse.}}

And we would get the following HTML output.

.. code-block:: html

   <p>They said that</p>
   <blockquote><p>I refuse.</p></blockquote>


Links and Images
================

Now it is time to expand on the form of a command in Paxter language.
To put a link on a piece of text, we use the command ``@link["target"]{...}``
where we put the actual target URL between quotation marks
and the actual displayed text still within the braces.
For example,

.. code-block:: paxter

   Click @link["http://example.com"]{here} to go to my website.

The above text in Paxter language will be transformed into the following HTML.

.. code-block:: html

   <p>Click <a href="http://example.com">here</a> to go to my website.</p>

Next, to insert an image, we use the command ``@image["srcpath", "alt"]``
where the first *argument* is the URL path to image wrapped between quotation marks,
and the second *argument* is the alternative text for the image when it goes missing.

.. code-block:: paxter

   @image["http://example.com/hello.png", "hello"]

The above Paxter text will be rendered into the following HTML.

.. code-block:: html

   <img src="http://example.com/hello.png" alt="hello" />


Lists
=====

Tables
======

Raw HTML
========

Escapes
=======

