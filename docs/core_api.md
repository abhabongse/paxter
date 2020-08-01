# Core API Reference

Paxter language package provides the following core functionality.

## Exceptions

Here are the list of exceptions raised from this library.

```eval_rst
.. autoclass:: paxter.exceptions.PaxterBaseException
   :members: message, positions
   :show-inheritance:

.. autoclass:: paxter.exceptions.PaxterConfigError
   :show-inheritance:

.. autoclass:: paxter.exceptions.PaxterSyntaxError
   :show-inheritance:

.. autoclass:: paxter.exceptions.PaxterRenderError
   :show-inheritance:

```

---

## Parsing

This class implements the parser for Paxter language.

```eval_rst
.. autoclass:: paxter.parser.ParseContext
   :members: input_text, tree
```

### Data Definitions

The result of the parsing yields the parsed tree consisting of the following classes.

```eval_rst
.. autoclass:: paxter.parser.Token
   :members: start_pos, end_pos
 
.. autoclass:: paxter.parser.Fragment
   :show-inheritance:

.. autoclass:: paxter.parser.TokenList
   :members: children
   :show-inheritance:

.. autoclass:: paxter.parser.Identifier
   :members: name
   :show-inheritance:

.. autoclass:: paxter.parser.Operator
   :members: symbols
   :show-inheritance:

.. autoclass:: paxter.parser.Number
   :members: value
   :show-inheritance:

.. autoclass:: paxter.parser.FragmentList
   :members: children, enclosing, at_prefix
   :show-inheritance:

.. autoclass:: paxter.parser.Text
   :members: inner, enclosing, at_prefix
   :show-inheritance:

.. autoclass:: paxter.parser.Command
   :members: starter, starter_enclosing, option, main_arg
   :show-inheritance:
```

### Other Utility Classes

Classes in this subsection is for reference only.

```eval_rst
.. autoclass:: paxter.parser.EnclosingPattern
   :members: left, right

.. autoclass:: paxter.parser.GlobalEnclosingPattern
   :members: left, right

.. autoclass:: paxter.parser.CharLoc
   :members: line, col
```

---

## Evaluation

This class implements the basic evaluator for Paxter language.

```eval_rst
.. autoclass:: paxter.evaluator.EvaluateContext
   :members: input_text, env, tree
```

### Function decorators

Wrappers for functions in python environments
to be used as function decorators.

```eval_rst
.. autoclass:: paxter.evaluator.BaseApply

.. autoclass:: paxter.evaluator.DirectApply
   :members: wrapped

.. autoclass:: paxter.evaluator.NormalApply
   :members: wrapped

.. autoclass:: paxter.evaluator.NormalApplyWithEnv
   :members: wrapped

```