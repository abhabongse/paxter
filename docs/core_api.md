# Core API Reference

Paxter language package provides the following core functionality.

## Parsing

This class implements the parser for Paxter language.

```eval_rst
.. autoclass:: paxter.core.ParseContext
   :members: input_text, tree
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
   :members: symbols
   :show-inheritance:

.. autoclass:: paxter.core.Number
   :members: value
   :show-inheritance:

.. autoclass:: paxter.core.FragmentList
   :members: children, enclosing, at_prefix
   :show-inheritance:

.. autoclass:: paxter.core.Text
   :members: inner, enclosing, at_prefix
   :show-inheritance:

.. autoclass:: paxter.core.Command
   :members: starter, starter_enclosing, option, main_arg
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
.. autoclass:: paxter.core.EnclosingPattern
   :members: left, right

.. autoclass:: paxter.core.GlobalEnclosingPattern
   :members: left, right

.. autoclass:: paxter.core.CharLoc
   :members: line, col
```
