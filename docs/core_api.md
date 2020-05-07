# Core API Reference

Paxter language package provides the following core functionality.

## Parsing

This class implements the parser for Paxter language.

```eval_rst
.. autoclass:: paxter.core.ParseContext
   :members: parse, input_text
```

## Data Definitions

The result of the parsing yields the parsed tree consisting of the following classes.

```eval_rst
.. autoclass:: paxter.core.Token
   :members: start_pos, end_pos
 
.. autoclass:: paxter.core.Fragment
   :show-inheritance:

.. autoclass:: paxter.core.TokenList
   :members: children
   :show-inheritance:

.. autoclass:: paxter.core.Identifier
   :members: name
   :show-inheritance:

.. autoclass:: paxter.core.Operator
   :members: symbol
   :show-inheritance:

.. autoclass:: paxter.core.Number
   :members: value
   :show-inheritance:

.. autoclass:: paxter.core.FragmentList
   :members: children, scope_pattern, is_command
   :show-inheritance:

.. autoclass:: paxter.core.Text
   :members: inner, scope_pattern, is_command
   :show-inheritance:

.. autoclass:: paxter.core.PaxterPhrase
   :members: inner, scope_pattern
   :show-inheritance:

.. autoclass:: paxter.core.PaxterApply
   :members: id, options, main_arg
   :show-inheritance:
```

## Exceptions

Here are the list of exceptions raised from this library.

```eval_rst
.. autoclass:: paxter.core.exceptions.PaxterBaseException
   :members: message, positions
   :show-inheritance:

.. autoclass:: paxter.core.exceptions.PaxterConfigError
   :show-inheritance:

.. autoclass:: paxter.core.exceptions.PaxterSyntaxError
   :show-inheritance:

.. autoclass:: paxter.core.exceptions.PaxterRenderError
   :show-inheritance:

```

## Other Utility Classes

Classes in this subsection is for reference only.

```eval_rst
.. autoclass:: paxter.core.ScopePattern
   :members: opening, closing

.. autoclass:: paxter.core.LineCol
   :members: line, col
```
