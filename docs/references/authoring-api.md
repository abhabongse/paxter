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

```{eval-rst}
.. autofunction:: paxter.authoring.run_simple_paxter

.. autofunction:: paxter.authoring.run_document_paxter
```

----

## Environment Creations

The following function creates a pre-defined unsafe Python environment dictionary
to be used with the evaluation context class.

```{eval-rst}
.. autofunction:: paxter.authoring.create_simple_env

.. autofunction:: paxter.authoring.create_document_env
```

----

## Evaluation Context Objects

The following instances are available in preset environments.

| Object | Alias | Simple Environment | Document Environment |
| ------ | ----- | ------------------ | -------------------- |
| `"@"` | `"@@"` | Yes | Yes |
| {func}`for_statement <paxter.authoring.controls.for_statement>` | **for** | Yes | Yes |
| {func}`if_statement <paxter.authoring.controls.if_statement>` | **if** | Yes | Yes |
| {func}`python_unsafe_exec <paxter.authoring.standards.python_unsafe_exec>` | **python** | Yes | Yes |
| {func}`verbatim <paxter.authoring.standards.verbatim>` | **verbatim** | Yes | Yes |
| {class}`RawElement <paxter.authoring.elements.RawElement>` | **raw** | - | Yes |
| {class}`Paragraph <paxter.authoring.elements.Paragraph>` | **paragraph** | - | Yes |
| {class}`Heading1 <paxter.authoring.elements.Heading1>` | **h1** | - | Yes |
| {class}`Heading2 <paxter.authoring.elements.Heading2>` | **h2** | - | Yes |
| {class}`Heading3 <paxter.authoring.elements.Heading3>` | **h3** | - | Yes |
| {class}`Heading4 <paxter.authoring.elements.Heading4>` | **h4** | - | Yes |
| {class}`Heading5 <paxter.authoring.elements.Heading5>` | **h5** | - | Yes |
| {class}`Heading6 <paxter.authoring.elements.Heading6>` | **h6** | - | Yes |
| {class}`Blockquote <paxter.authoring.elements.Blockquote>` | **blockquote** | - | Yes |
| {class}`Bold <paxter.authoring.elements.Bold>` | **bold** | - | Yes |
| {class}`Italic <paxter.authoring.elements.Italic>` | **italic** | - | Yes |
| {class}`Underline <paxter.authoring.elements.Underline>` | **uline** | - | Yes |
| {class}`Code <paxter.authoring.elements.Code>` | **code** | - | Yes |
| {class}`Link <paxter.authoring.elements.Link>` | **link** | - | Yes |
| {class}`Image <paxter.authoring.elements.Image>` | **image** | - | Yes |
| {class}`NumberedList <paxter.authoring.elements.NumberedList>` | **numbered_list** | - | Yes |
| {class}`BulletedList <paxter.authoring.elements.BulletedList>` | **bulleted_list** | - | Yes |
| {class}`Table <paxter.authoring.elements.Table>` | **table** | - | Yes |
| {class}`TableHeader <paxter.authoring.elements.TableHeader>` | **table_header** | - | Yes |
| {class}`TableRow <paxter.authoring.elements.TableRow>` | **table_row** | - | Yes |
| {data}`horizontal_rule <paxter.authoring.elements.horizontal_rule>` | **hrule** | - | Yes |
| {data}`line_break <paxter.authoring.elements.line_break>` | **line_break** or `"@\"` | - | Yes |
| {data}`non_breaking_space <paxter.authoring.elements.non_breaking_space>` | **nbsp** or `"@%"` | - | Yes |
| {data}`hair_space <paxter.authoring.elements.hair_space>` | **hairsp** or `"@."` | - | Yes |
| {data}`thin_space <paxter.authoring.elements.thin_space>` | **thinsp** or `"@,"` | - | Yes |

### Control Functions

```{eval-rst}
.. autofunction:: paxter.authoring.controls.for_statement

.. autofunction:: paxter.authoring.controls.if_statement
```

### Standard Functions

```{eval-rst}
.. autofunction:: paxter.authoring.standards.phrase_unsafe_eval

.. autofunction:: paxter.authoring.standards.python_unsafe_exec

.. autofunction:: paxter.authoring.standards.verbatim
```

### Element Data Classes

```{eval-rst}
.. autoclass:: paxter.authoring.elements.Element
   :members:

.. autoclass:: paxter.authoring.elements.RawElement
   :show-inheritance:

.. autoclass:: paxter.authoring.elements.SimpleElement
   :members: HTML_OPENING, HTML_CLOSING, from_fragments, from_direct_args
   :show-inheritance:

.. autoclass:: paxter.authoring.elements.EnumeratingElement
   :members: HTML_GLOBAL_OPENING, HTML_GLOBAL_CLOSING, HTML_ITEM_OPENING, HTML_ITEM_CLOSING, from_direct_args
   :show-inheritance:

.. autoclass:: paxter.authoring.elements.Document
   :show-inheritance:

.. autoclass:: paxter.authoring.elements.Paragraph
   :show-inheritance:

.. autoclass:: paxter.authoring.elements.Heading1
   :show-inheritance:

.. autoclass:: paxter.authoring.elements.Heading2
   :show-inheritance:

.. autoclass:: paxter.authoring.elements.Heading3
   :show-inheritance:

.. autoclass:: paxter.authoring.elements.Heading4
   :show-inheritance:

.. autoclass:: paxter.authoring.elements.Heading5
   :show-inheritance:

.. autoclass:: paxter.authoring.elements.Heading6
   :show-inheritance:


.. autoclass:: paxter.authoring.elements.Bold
   :show-inheritance:

.. autoclass:: paxter.authoring.elements.Italic
   :show-inheritance:

.. autoclass:: paxter.authoring.elements.Underline
   :show-inheritance:

.. autoclass:: paxter.authoring.elements.Code
   :show-inheritance:

.. autoclass:: paxter.authoring.elements.Blockquote
   :members: from_fragments
   :show-inheritance:

.. autoclass:: paxter.authoring.elements.Link
   :members: from_fragments
   :show-inheritance:

.. autoclass:: paxter.authoring.elements.Image
   :show-inheritance:

.. autoclass:: paxter.authoring.elements.NumberedList
   :show-inheritance:

.. autoclass:: paxter.authoring.elements.BulletedList
   :show-inheritance:

.. autoclass:: paxter.authoring.elements.Table
   :show-inheritance:

.. autoclass:: paxter.authoring.elements.TableHeader
   :show-inheritance:

.. autoclass:: paxter.authoring.elements.TableRow
   :show-inheritance:

.. autodata:: paxter.authoring.elements.line_break

.. autodata:: paxter.authoring.elements.horizontal_rule

.. autodata:: paxter.authoring.elements.non_breaking_space

.. autodata:: paxter.authoring.elements.hair_space

.. autodata:: paxter.authoring.elements.thin_space
```
