##############
Quick Blogging
##############

To quickly get started with blogging or writing an article,
we introduce the Paxter language syntax
as being *preconfigured* by :mod:`paxter.author` subpackage
which can be used to write rich-formatted content.

.. important::

   Most of the descriptions about the syntax shown on this page
   are specific to the preconfigured variation of Paxter language
   provided by :mod:`paxter.author` subpackage.
   It is actually *not* tied to the core Paxter language specification.

   Paxter library (which includes the core Paxter language specification)
   is designed to be very extensible and customizable.
   The :mod:`paxter.author` subpackage is merely
   supplementary provided by Paxter library for convenience.
   It is entirely possible to utilize Paxter library *without* touching
   any of the :mod:`paxter.author` whatsoever,
   as being demonstrated in the
   :doc:`intermediate tutorials <../intermediate-tutorials/index>` section.


Command: A Basic Building Block
===============================

**A command** is the core building block in Paxter language.
It has various syntactical forms, but all of them have the same basic principles:

- Each command always begin with an ``@`` symbol in the source text.
- Each command always has the **phrase part**
  which immediately follows the initial ``@`` symbol.
- Each command may optionally have what is called the **options part**.
  If it exists, it has the form of ``[...]`` that follows the phrase part.
- Each command may optionally have what is called the **main argument part**.
  If it exists, it follows the phrase part
  or the options part (if the options part exists).

This may sound confusing right now.
Hopefully things will get clearer as we discuss
the specific syntax in the upcoming sections.

.. important::

   A rule of thumb to remember about the core Paxter language
   is that it dictates only how a command in the source text should be parsed.
   It has no bearing on how each parsed command and any other raw text
   are to be interpreted or evaluated into the desired final output.
   For descriptions of syntax appeared on this page,
   this interpretation is done by the supplementary :mod:`paxter.author` subpackage.


Bolds, Italics, and Underline
=============================

Let us begin with “bolding” part of a source text.
We use the command ``@bold{...}``,
replacing ``...`` with the actual text to be emphasized.
In this particular command, ``bold`` is the phrase part
whereas the emphasized text is the main argument part of the command.

For example, consider the following source text written in Paxter language.

.. code-block:: paxter

   This is a very @bold{important part} of the statement.

This source text will be transformed to the following HTML output.

.. code-block:: html

   <p>This is a very <b>important part</b> of the statement.</p>

And likewise, for italicized text and underlined text,
use the command ``@italic{...}`` and ``@uline{...}`` respectively.
Notice that we altered the phrase part of the command
while the the main argument parts remains the same.

.. code-block:: paxter

   This is a very @italic{important part} of @uline{the statement}.

This source text will be transformed to the following HTML output.

.. code-block:: html

   <p>This is a very <i>important part</i> of <u>the statement</u>.</p>


Nested commands
---------------

One nice thing about Paxter command is that they are allowed
to be nested inside the main argument between the pair of curly braces.
For example,

.. code-block:: paxter

   This is @italic{so important that @uline{multiple emphasis} is required}.

When the above source text get rendered into HTML,
we obtain the following result.

.. code-block:: html

   <p>This is <i>so important that <u>multiple emphasis</u> is required</i>.</p>


Monospaced Code
===============

Similarly to what we have seen with
``@bold{...}``, ``@italic{...}``, and ``@uline{...}`` from above,
we use the command ``@code{...}`` to encapsulate text
to be displayed as monospaced code.

For example, the following source text written in Paxter language

.. code-block:: paxter

   Run the @code{python} command.

will be evaluated into the HTML output shown below.

.. code-block:: html

   <p>Run the <code>python</code> command.</p>


Multiple Paragraphs
===================

To write multiple paragraphs,
simply separate chunks of texts with at least two newline characters
(i.e. there must be a blank line between consecutive paragraphs).
Each chunk of text will result in its own paragraph.
Consider the following example containing exactly three paragraphs.

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

.. important::

   The implicit paragraph splitting behavior of the source text
   is preconfigured by the supplementary :mod:`paxter.author` subpackage
   and has nothing to do with the core Paxter language specification.


Headings
========

To include a heading (from level 1 to level 6)
use the command ``@h1{...}`` through ``@h6{...}`` on its own chunk.
They must be separated from other paragraph chunks
with at least one blank line.

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

Observe that if the ``@h1{...}`` and ``@h2{...}`` were *not* used
to encapsulate the heading text,
they would have been rendered as its own paragraph.
Try that for yourself.

Also, what happens if the command ``@h1{...}``
accidentally did *not* surround the entire chunk of text?
Let us look at this example in which
the exclamation mark is located *outside* of the command:

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

The ``@blockquote{...}`` command must reside on its own chunk
just like a heading command.
So the following Paxter source text

.. code-block:: paxter

   They said that

   @blockquote{I refuse.}

would be transformed into the following HTML output.

.. code-block:: html

   <p>They said that</p>
   <blockquote>I refuse.</blockquote>

However, suppose that we want to include multiple paragraphs inside the blockquote.
We can follow the similar rules
as to how to write multiple paragraphs in general:
by separating them with at least two newline characters.
This is demonstrated in the following example.

.. code-block:: paxter

   They said that

   @blockquote{
       I refuse.

       Then I regret.
   }

.. code-block:: html

   <p>They said that</p>
   <blockquote>
       <p>I refuse.</p>
       <p>Then I regret.</p>
   </blockquote>

The important key to note here is that,
each paragraph within the blockquote will be surrounded by
a paragraph tag ``<p>...</p>``
as long as more than one chunk of text exists.

.. todo::

   Continue here.

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

