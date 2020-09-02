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
.. autofunction:: paxter.author.preset.run_simple_paxter

.. autofunction:: paxter.author.preset.run_document_paxter
```

----

## Environment Creations

The following function creates a pre-defined unsafe Python environment dictionary
to be used with the evaluation context class.

```{eval-rst}
.. autofunction:: paxter.author.environ.create_simple_env

.. autofunction:: paxter.author.environ.create_document_env
```

----

## Evaluation Context Objects

The following instances are available in preset environments.

| Object | Alias | Simple Environment | Document Environment |
| ------ | ----- | ------------------ | -------------------- |
| `"@"` | `"@@"` | Yes | Yes |
| {func}`for_statement <paxter.author.controls.for_statement>` | **for** | Yes | Yes |
| {func}`if_statement <paxter.author.controls.if_statement>` | **if** | Yes | Yes |
| {func}`python_unsafe_exec <paxter.author.standards.python_unsafe_exec>` | **python** | Yes | Yes |
| {func}`verbatim <paxter.author.standards.verbatim>` | **verbatim** | Yes | Yes |
| {class}`RawElement <paxter.author.elements.RawElement>` | **raw** | - | Yes |
| {class}`Paragraph <paxter.author.elements.Paragraph>` | **paragraph** | - | Yes |
| {class}`Heading1 <paxter.author.elements.Heading1>` | **h1** | - | Yes |
| {class}`Heading2 <paxter.author.elements.Heading2>` | **h2** | - | Yes |
| {class}`Heading3 <paxter.author.elements.Heading3>` | **h3** | - | Yes |
| {class}`Heading4 <paxter.author.elements.Heading4>` | **h4** | - | Yes |
| {class}`Heading5 <paxter.author.elements.Heading5>` | **h5** | - | Yes |
| {class}`Heading6 <paxter.author.elements.Heading6>` | **h6** | - | Yes |
| {class}`Blockquote <paxter.author.elements.Blockquote>` | **blockquote** | - | Yes |
| {class}`Bold <paxter.author.elements.Bold>` | **bold** | - | Yes |
| {class}`Italic <paxter.author.elements.Italic>` | **italic** | - | Yes |
| {class}`Underline <paxter.author.elements.Underline>` | **uline** | - | Yes |
| {class}`Code <paxter.author.elements.Code>` | **code** | - | Yes |
| {class}`Link <paxter.author.elements.Link>` | **link** | - | Yes |
| {class}`Image <paxter.author.elements.Image>` | **image** | - | Yes |
| {class}`NumberedList <paxter.author.elements.NumberedList>` | **numbered_list** | - | Yes |
| {class}`BulletedList <paxter.author.elements.BulletedList>` | **bulleted_list** | - | Yes |
| {class}`Table <paxter.author.elements.Table>` | **table** | - | Yes |
| {class}`TableHeader <paxter.author.elements.TableHeader>` | **table_header** | - | Yes |
| {class}`TableRow <paxter.author.elements.TableRow>` | **table_row** | - | Yes |
| {data}`horizontal_rule <paxter.author.elements.horizontal_rule>` | **hrule** | - | Yes |
| {data}`line_break <paxter.author.elements.line_break>` | **line_break** or `"@\"` | - | Yes |
| {data}`non_breaking_space <paxter.author.elements.non_breaking_space>` | **nbsp** or `"@%"` | - | Yes |
| {data}`hair_space <paxter.author.elements.hair_space>` | **hairsp** or `"@."` | - | Yes |
| {data}`thin_space <paxter.author.elements.thin_space>` | **thinsp** or `"@,"` | - | Yes |

### Control Functions

```{eval-rst}
.. autofunction:: paxter.author.controls.for_statement

.. autofunction:: paxter.author.controls.if_statement
```

### Standard Functions

```{eval-rst}
.. autofunction:: paxter.author.standards.phrase_unsafe_eval

.. autofunction:: paxter.author.standards.python_unsafe_exec

.. autofunction:: paxter.author.standards.verbatim
```

### Element Data Classes

```{eval-rst}
.. autoclass:: paxter.author.elements.Element
   :members:

.. autoclass:: paxter.author.elements.RawElement
   :show-inheritance:

.. autoclass:: paxter.author.elements.SimpleElement
   :members: HTML_OPENING, HTML_CLOSING, from_fragments, from_direct_args
   :show-inheritance:

.. autoclass:: paxter.author.elements.EnumeratingElement
   :members: HTML_GLOBAL_OPENING, HTML_GLOBAL_CLOSING, HTML_ITEM_OPENING, HTML_ITEM_CLOSING, from_direct_args
   :show-inheritance:

.. autoclass:: paxter.author.elements.Document
   :show-inheritance:

.. autoclass:: paxter.author.elements.Paragraph
   :show-inheritance:

.. autoclass:: paxter.author.elements.Heading1
   :show-inheritance:

.. autoclass:: paxter.author.elements.Heading2
   :show-inheritance:

.. autoclass:: paxter.author.elements.Heading3
   :show-inheritance:

.. autoclass:: paxter.author.elements.Heading4
   :show-inheritance:

.. autoclass:: paxter.author.elements.Heading5
   :show-inheritance:

.. autoclass:: paxter.author.elements.Heading6
   :show-inheritance:

.. autoclass:: paxter.author.elements.Bold
   :show-inheritance:

.. autoclass:: paxter.author.elements.Italic
   :show-inheritance:

.. autoclass:: paxter.author.elements.Underline
   :show-inheritance:

.. autoclass:: paxter.author.elements.Code
   :show-inheritance:

.. autoclass:: paxter.author.elements.Blockquote
   :members: from_fragments
   :show-inheritance:

.. autoclass:: paxter.author.elements.Link
   :members: from_fragments
   :show-inheritance:

.. autoclass:: paxter.author.elements.Image
   :show-inheritance:

.. autoclass:: paxter.author.elements.NumberedList
   :show-inheritance:

.. autoclass:: paxter.author.elements.BulletedList
   :show-inheritance:

.. autoclass:: paxter.author.elements.Table
   :show-inheritance:

.. autoclass:: paxter.author.elements.TableHeader
   :show-inheritance:

.. autoclass:: paxter.author.elements.TableRow
   :show-inheritance:

.. autodata:: paxter.author.elements.line_break

.. autodata:: paxter.author.elements.horizontal_rule

.. autodata:: paxter.author.elements.non_breaking_space

.. autodata:: paxter.author.elements.hair_space

.. autodata:: paxter.author.elements.thin_space
```
