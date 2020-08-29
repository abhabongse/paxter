###############
Getting Started
###############

Installation
============

Paxter python package can be installed from PyPI via the following ``pip`` command.
Of course, we can also opt for other methods of python package managements.

.. code-block:: bash

   $ pip install paxter

Next, let us write a basic blog entry.


Writing The First Blog Entry
============================

Suppose that we are going to write a blog post
under Paxter language syntax as shown in the following.
Let us ignore the specific details about the syntax for now
as we will discuss them further on the next page.

.. code-block:: paxter

   @h1{New Blog!}

   Welcome to our new blog website.
   @italic{Please keep watching this space for content.}

The above content is expected to be rendered into the following result.

.. raw:: html

   <blockquote style="padding-left: 40px;">
           <h1>New Blog!</h1>
           <p>Welcome to our new blog website.
              <i>Please keep watching this space for content.</i>
           </p>
   </blockquote>

Here are a few ways that we can transform the original Paxter source code
into the final HTML output.


Method 1: Command Line
----------------------

Suppose that the Paxter source code (as shown above)
is stored within the file called ``new-blog.paxter``.
Once Paxter package is installed,
we can run the command ``paxter html`` to render the HTML output.

.. code-block:: console

   $ cat new-blog.paxter
   @h1{New Blog!}

   Welcome to our new blog website.
   @italic{Please keep watching this space for content.}

   $ paxter html -i new-blog.paxter
   <h1>New Blog!</h1><p>Welcome to our new blog website.
   <i>Please keep watching this space for content.</i></p>


Method 2: Programmatic Usage
----------------------------

A more flexible way to transform Paxter source text into HTML output
is to make calls the API functions provided by Paxter library.
The easiest way is to do the following.

.. code-block:: python

   from paxter.author import run_document_paxter

   # The following source text is read from a source file.
   # However, in reality, source text may be read from other sources
   # such as some databases or even fetched via some content management API.
   with open("new-blog.paxter") as fobj:
       source_text = fobj.read()

   document = run_document_paxter(source_text)
   html_output = document.html()

.. code-block:: pycon

   >>> print(html_output)
   <h1>New Blog!</h1><p>Welcome to our new blog website.
   <i>Please keep watching this space for content.</i></p>

This approach shown here is merely the very basic usage
of Paxter library with *preconfigured* settings.
More advanced programmatic usage will be discussed later.
