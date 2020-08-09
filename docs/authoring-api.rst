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

.. autofunction:: paxter.authoring.preset.run_simple_paxter

.. autofunction:: paxter.authoring.preset.run_document_paxter

----


Environment Creations
=====================

The following function creates a pre-defined unsafe Python environment dictionary
to be used with the evaluation context class.

.. autofunction:: paxter.authoring.environ.create_simple_env

.. autofunction:: paxter.authoring.environ.create_document_env

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
   * - :func:`python_unsafe_exec <paxter.authoring.standards.python_unsafe_exec>`
     - **python**
     - Yes
     - Yes
   * - :func:`verbatim <paxter.authoring.standards.verbatim>`
     - **verbatim**
     - Yes
     - Yes
   * - :func:`if_statement <paxter.authoring.controls.if_statement>`
     - **if**
     - Yes
     - Yes
   * - :func:`for_statement <paxter.authoring.controls.for_statement>`
     - **for**
     - Yes
     - Yes
   * - :class:`RawElement <paxter.authoring.document.RawElement>`
     - **raw**
     - \-
     - Yes
   * - :data:`line_break <paxter.authoring.document.line_break>`
     - **break**
     - \-
     - Yes
   * - :data:`horizontal_rule <paxter.authoring.document.horizontal_rule>`
     - **hrule**
     - \-
     - Yes
   * - :data:`non_breaking_space <paxter.authoring.document.non_breaking_space>`
     - **nbsp**, ‘**%**’
     - \-
     - Yes
   * - :data:`hair_space <paxter.authoring.document.hair_space>`
     - **hairsp**, ‘**.**’
     - \-
     - Yes
   * - :data:`thin_space <paxter.authoring.document.thin_space>`
     - **thinsp**, ‘**,**’
     - \-
     - Yes
   * - :class:`Paragraph <paxter.authoring.document.Paragraph>`
     - **paragraph**
     - \-
     - Yes
   * - :class:`Heading1 <paxter.authoring.document.Heading1>`
     - **h1**
     - \-
     - Yes
   * - :class:`Heading2 <paxter.authoring.document.Heading2>`
     - **h2**
     - \-
     - Yes
   * - :class:`Heading3 <paxter.authoring.document.Heading3>`
     - **h3**
     - \-
     - Yes
   * - :class:`Heading4 <paxter.authoring.document.Heading4>`
     - **h4**
     - \-
     - Yes
   * - :class:`Heading5 <paxter.authoring.document.Heading5>`
     - **h5**
     - \-
     - Yes
   * - :class:`Heading6 <paxter.authoring.document.Heading6>`
     - **h6**
     - \-
     - Yes
   * - :class:`Bold <paxter.authoring.document.Bold>`
     - **bold**
     - \-
     - Yes
   * - :class:`Heading6 <paxter.authoring.document.Italic>`
     - **italic**
     - \-
     - Yes
   * - :class:`Underline <paxter.authoring.document.Underline>`
     - **uline**
     - \-
     - Yes
   * - :class:`Code <paxter.authoring.document.Code>`
     - **code**
     - \-
     - Yes
   * - :class:`Blockquote <paxter.authoring.document.Blockquote>`
     - **blockquote**
     - \-
     - Yes
   * - :class:`Link <paxter.authoring.document.Link>`
     - **link**
     - \-
     - Yes
   * - :class:`Image <paxter.authoring.document.Image>`
     - **image**
     - \-
     - Yes
   * - :class:`NumberedList <paxter.authoring.document.NumberedList>`
     - **numbered_list**
     - \-
     - Yes
   * - :class:`BulletedList <paxter.authoring.document.BulletedList>`
     - **bulleted_list**
     - \-
     - Yes


Standard Functions
------------------

.. autofunction:: paxter.authoring.standards.phrase_unsafe_eval

.. autofunction:: paxter.authoring.standards.python_unsafe_exec

.. autofunction:: paxter.authoring.standards.verbatim


Control Functions
-----------------

.. autofunction:: paxter.authoring.controls.if_statement

.. autofunction:: paxter.authoring.controls.for_statement


Document Data Classes
---------------------

.. autoclass:: paxter.authoring.document.Element
   :members:

.. autoclass:: paxter.authoring.document.Document
   :show-inheritance:

.. autoclass:: paxter.authoring.document.RawElement
   :show-inheritance:

.. autodata:: paxter.authoring.document.line_break

.. autodata:: paxter.authoring.document.horizontal_rule

.. autodata:: paxter.authoring.document.non_breaking_space

.. autodata:: paxter.authoring.document.hair_space

.. autodata:: paxter.authoring.document.thin_space

.. autoclass:: paxter.authoring.document.SimpleElement
   :members: HTML_OPENING, HTML_CLOSING
   :show-inheritance:

.. autoclass:: paxter.authoring.document.Paragraph
   :show-inheritance:

.. autoclass:: paxter.authoring.document.Heading1
   :show-inheritance:

.. autoclass:: paxter.authoring.document.Heading2
   :show-inheritance:

.. autoclass:: paxter.authoring.document.Heading3
   :show-inheritance:

.. autoclass:: paxter.authoring.document.Heading4
   :show-inheritance:

.. autoclass:: paxter.authoring.document.Heading5
   :show-inheritance:

.. autoclass:: paxter.authoring.document.Heading6
   :show-inheritance:

.. autoclass:: paxter.authoring.document.Bold
   :show-inheritance:

.. autoclass:: paxter.authoring.document.Italic
   :show-inheritance:

.. autoclass:: paxter.authoring.document.Underline
   :show-inheritance:

.. autoclass:: paxter.authoring.document.Code
   :show-inheritance:

.. autoclass:: paxter.authoring.document.Blockquote
   :show-inheritance:

.. autoclass:: paxter.authoring.document.Link
   :show-inheritance:

.. autoclass:: paxter.authoring.document.Image
   :show-inheritance:

.. autoclass:: paxter.authoring.document.BareList
   :show-inheritance:

.. autoclass:: paxter.authoring.document.NumberedList
   :show-inheritance:

.. autoclass:: paxter.authoring.document.BulletedList
   :show-inheritance:
