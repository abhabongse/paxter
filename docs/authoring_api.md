# Authoring API Reference

All of the following functions and classes 
are not part of the core Paxter language.
They are provided only for convenience;
it is entirely possible to utilize Paxter package 
without using any of the following functions.
Users are encouraged to read source code of these functions
to learn how to reassemble core APIs to suit their needs.

## Preset Functions

The following function combines Paxter language parsing
together with parsed tree evaluation.

```eval_rst
.. autofunction:: paxter.preset.run_simple_paxter

.. autofunction:: paxter.preset.run_document_paxter
```

---

## Environment Creations

The following function creates a pre-defined unsafe Python environment dictionary 
to be used with the evaluation context class.

```eval_rst
.. autofunction:: paxter.authoring.environ.create_simple_env

.. autofunction:: paxter.authoring.environ.create_document_env
```

---

## Evaluation Context Functions and Classes

The following functions and classes are available in preset environments.


```eval_rst
.. list-table::
   :widths: auto
   :header-rows: 1
   :align: center

   * - Function or Class
     - Alias
     - Simple Env
     - Document Env
   * - :func:`python_unsafe_exec <paxter.authoring.standards.python_unsafe_exec>`
     - **python**
     - Yes
     - Yes
   * - :func:`flatten <paxter.authoring.standards.flatten>`
     - **flatten**
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
     - **nbsp** (@%)
     - \-
     - Yes
   * - :data:`hair_space <paxter.authoring.document.hair_space>`
     - **hairsp** (@.)
     - \-
     - Yes
   * - :data:`thin_space <paxter.authoring.document.thin_space>`
     - **thinsp** (@,)
     - \-
     - Yes
   * - Empty string (``""``)
     - @!
     - \-
     - Yes
   * - @-symbol (``"@"``)
     - @@
     - \-
     - Yes


.. todo::

   Add more contents.
```

### Standard Functions

```eval_rst
.. autofunction:: paxter.authoring.standards.starter_unsafe_eval

.. autofunction:: paxter.authoring.standards.python_unsafe_exec

.. autofunction:: paxter.authoring.standards.flatten

.. autofunction:: paxter.authoring.standards.verbatim
```

### Control Functions

```eval_rst
.. autofunction:: paxter.authoring.controls.if_statement

.. autofunction:: paxter.authoring.controls.for_statement
```

### Document Data Classes

```eval_rst
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
```