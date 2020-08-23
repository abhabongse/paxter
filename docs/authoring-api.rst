#######################
Authoring API Reference
#######################

All of the following functions and classes 
are not part of the core Paxter language.
They are provided only for convenience;
it is entirely possible to utilize Paxter package 
without using any of the following functions.
Users are encouraged to read source code of these functions
to learn how to reassemble core APIs to suit their needs.

Preset Functions
================

The following function combines Paxter language parsing
together with parsed tree evaluation.

.. autofunction:: paxter.author.preset.run_simple_paxter

.. autofunction:: paxter.author.preset.run_document_paxter

----


Environment Creations
=====================

The following function creates a pre-defined unsafe Python environment dictionary
to be used with the evaluation context class.

.. autofunction:: paxter.author.environ.create_simple_env

.. autofunction:: paxter.author.environ.create_document_env

----


Evaluation Context Objects
==========================

The following instances are available in preset environments.

.. list-table::
   :widths: auto
   :header-rows: 1
   :align: center

   * - Object
     - Alias
     - Simple Env
     - Document Env
   * - ``"@"``
     - ‘**@**’
     - Yes
     - Yes
   * - :func:`python_unsafe_exec <paxter.author.standards.python_unsafe_exec>`
     - **python**
     - Yes
     - Yes
   * - :func:`verbatim <paxter.author.standards.verbatim>`
     - **verbatim**
     - Yes
     - Yes
   * - :func:`if_statement <paxter.author.controls.if_statement>`
     - **if**
     - Yes
     - Yes
   * - :func:`for_statement <paxter.author.controls.for_statement>`
     - **for**
     - Yes
     - Yes
   * - :class:`RawElement <paxter.author.document.RawElement>`
     - **raw**
     - \-
     - Yes
   * - :data:`line_break <paxter.author.document.line_break>`
     - **break**
     - \-
     - Yes
   * - :data:`horizontal_rule <paxter.author.document.horizontal_rule>`
     - **hrule**
     - \-
     - Yes
   * - :data:`non_breaking_space <paxter.author.document.non_breaking_space>`
     - **nbsp**, ‘**%**’
     - \-
     - Yes
   * - :data:`hair_space <paxter.author.document.hair_space>`
     - **hairsp**, ‘**.**’
     - \-
     - Yes
   * - :data:`thin_space <paxter.author.document.thin_space>`
     - **thinsp**, ‘**,**’
     - \-
     - Yes
   * - :class:`Paragraph <paxter.author.document.Paragraph>`
     - **paragraph**
     - \-
     - Yes
   * - :class:`Heading1 <paxter.author.document.Heading1>`
     - **h1**
     - \-
     - Yes
   * - :class:`Heading2 <paxter.author.document.Heading2>`
     - **h2**
     - \-
     - Yes
   * - :class:`Heading3 <paxter.author.document.Heading3>`
     - **h3**
     - \-
     - Yes
   * - :class:`Heading4 <paxter.author.document.Heading4>`
     - **h4**
     - \-
     - Yes
   * - :class:`Heading5 <paxter.author.document.Heading5>`
     - **h5**
     - \-
     - Yes
   * - :class:`Heading6 <paxter.author.document.Heading6>`
     - **h6**
     - \-
     - Yes
   * - :class:`Bold <paxter.author.document.Bold>`
     - **bold**
     - \-
     - Yes
   * - :class:`Heading6 <paxter.author.document.Italic>`
     - **italic**
     - \-
     - Yes
   * - :class:`Underline <paxter.author.document.Underline>`
     - **uline**
     - \-
     - Yes
   * - :class:`Code <paxter.author.document.Code>`
     - **code**
     - \-
     - Yes
   * - :class:`Blockquote <paxter.author.document.Blockquote>`
     - **blockquote**
     - \-
     - Yes
   * - :class:`Link <paxter.author.document.Link>`
     - **link**
     - \-
     - Yes
   * - :class:`Image <paxter.author.document.Image>`
     - **image**
     - \-
     - Yes
   * - :class:`NumberedList <paxter.author.document.NumberedList>`
     - **numbered_list**
     - \-
     - Yes
   * - :class:`BulletedList <paxter.author.document.BulletedList>`
     - **bulleted_list**
     - \-
     - Yes


Standard Functions
------------------

.. autofunction:: paxter.author.standards.phrase_unsafe_eval

.. autofunction:: paxter.author.standards.python_unsafe_exec

.. autofunction:: paxter.author.standards.verbatim


Control Functions
-----------------

.. autofunction:: paxter.author.controls.if_statement

.. autofunction:: paxter.author.controls.for_statement


Document Data Classes
---------------------

.. autoclass:: paxter.author.document.Element
   :members:

.. autoclass:: paxter.author.document.Document
   :show-inheritance:

.. autoclass:: paxter.author.document.RawElement
   :show-inheritance:

.. autodata:: paxter.author.document.line_break

.. autodata:: paxter.author.document.horizontal_rule

.. autodata:: paxter.author.document.non_breaking_space

.. autodata:: paxter.author.document.hair_space

.. autodata:: paxter.author.document.thin_space

.. autoclass:: paxter.author.document.SimpleElement
   :members: HTML_OPENING, HTML_CLOSING
   :show-inheritance:

.. autoclass:: paxter.author.document.Paragraph
   :show-inheritance:

.. autoclass:: paxter.author.document.Heading1
   :show-inheritance:

.. autoclass:: paxter.author.document.Heading2
   :show-inheritance:

.. autoclass:: paxter.author.document.Heading3
   :show-inheritance:

.. autoclass:: paxter.author.document.Heading4
   :show-inheritance:

.. autoclass:: paxter.author.document.Heading5
   :show-inheritance:

.. autoclass:: paxter.author.document.Heading6
   :show-inheritance:

.. autoclass:: paxter.author.document.Bold
   :show-inheritance:

.. autoclass:: paxter.author.document.Italic
   :show-inheritance:

.. autoclass:: paxter.author.document.Underline
   :show-inheritance:

.. autoclass:: paxter.author.document.Code
   :show-inheritance:

.. autoclass:: paxter.author.document.Blockquote
   :show-inheritance:

.. autoclass:: paxter.author.document.Link
   :show-inheritance:

.. autoclass:: paxter.author.document.Image
   :show-inheritance:

.. autoclass:: paxter.author.document.SequenceElement
   :show-inheritance:

.. autoclass:: paxter.author.document.HigherSequenceElement
   :show-inheritance:

.. autoclass:: paxter.author.document.NumberedList
   :show-inheritance:

.. autoclass:: paxter.author.document.BulletedList
   :show-inheritance:

.. autoclass:: paxter.author.document.Table
   :show-inheritance:

.. autoclass:: paxter.author.document.TableHeader
   :show-inheritance:

.. autoclass:: paxter.author.document.TableRow
   :show-inheritance:
