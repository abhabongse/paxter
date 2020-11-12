# Core API Reference

Paxter language package provides the following core functionality.

## Parsing

The following class is where the main Paxter language parsing logic happens.

```{eval-rst}
.. autofunction:: paxter.parsing.parse
```

(parsing-data-definitions)=
### Data Definitions

Results of the Paxter language parsing yields parsed trees
which consist of instances of the following data classes.

```{eval-rst}
.. autoclass:: paxter.parsing.Token
   :members: start_pos, end_pos
 
.. autoclass:: paxter.parsing.Fragment
   :show-inheritance:

.. autoclass:: paxter.parsing.TokenSeq
   :members: children
   :show-inheritance:

.. autoclass:: paxter.parsing.Identifier
   :members: name
   :show-inheritance:

.. autoclass:: paxter.parsing.Operator
   :members: symbols
   :show-inheritance:

.. autoclass:: paxter.parsing.Number
   :members: value
   :show-inheritance:

.. autoclass:: paxter.parsing.FragmentSeq
   :members: children, enclosing
   :show-inheritance:

.. autoclass:: paxter.parsing.Text
   :members: inner, enclosing
   :show-inheritance:

.. autoclass:: paxter.parsing.Command
   :members: phrase, phrase_enclosing, options, main_arg
   :show-inheritance:
```

### Other Utility Classes

Other classes related to parsing,
presented here for reference only.

```{eval-rst}
.. autoclass:: paxter.parsing.CharLoc
   :members: line, col

.. autoclass:: paxter.parsing.enclosing.EnclosingPattern
   :members: left, right

.. autoclass:: paxter.parsing.enclosing.GlobalEnclosingPattern
   :members: left, right
   :show-inheritance:
```

## Evaluation

The following class implements the basic tree evaluation in Paxter language.
Users may want to extend this class to override the tree evaluation.

```{eval-rst}
.. autoclass:: paxter.interpreting.context.InterpreterContext
   :members:
```

The evaluated list of fragments will be of the following type

```{eval-rst}
.. autoclass:: paxter.interpreting.FragmentList
   :members:
   :show-inheritance:
```

### Function decorators

Wrappers for functions in python environments
to be used as function decorators.

```{eval-rst}
.. autoclass:: paxter.interpreting.BaseApply

.. autoclass:: paxter.interpreting.DirectApply
   :show-inheritance:

.. autoclass:: paxter.interpreting.NormalApply
   :show-inheritance:

.. autoclass:: paxter.interpreting.NormalApplyWithEnv
   :show-inheritance:
```

----

## Exceptions

These are all the exception classes raised from this library package.

```{eval-rst}
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
