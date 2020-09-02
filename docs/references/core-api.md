# Core API Reference

Paxter language package provides the following core functionality.

## Parsing

The following class is where the main Paxter language parsing logic happens.

```{eval-rst}
.. autoclass:: paxter.parse.ParseContext
   :members: input_text, tree
```

(parsing-data-definitions)=
### Data Definitions

Results of the Paxter language parsing yields parsed trees
which consist of instances of the following data classes.

```{eval-rst}
.. autoclass:: paxter.parse.data.Token
   :members: start_pos, end_pos
 
.. autoclass:: paxter.parse.data.Fragment
   :show-inheritance:

.. autoclass:: paxter.parse.data.TokenSeq
   :members: children
   :show-inheritance:

.. autoclass:: paxter.parse.data.Identifier
   :members: name
   :show-inheritance:

.. autoclass:: paxter.parse.data.Operator
   :members: symbols
   :show-inheritance:

.. autoclass:: paxter.parse.data.Number
   :members: value
   :show-inheritance:

.. autoclass:: paxter.parse.data.FragmentSeq
   :members: children, enclosing
   :show-inheritance:

.. autoclass:: paxter.parse.data.Text
   :members: inner, enclosing
   :show-inheritance:

.. autoclass:: paxter.parse.data.Command
   :members: phrase, phrase_enclosing, options, main_arg
   :show-inheritance:
```

### Other Utility Classes

Other classes related to parsing,
presented here for reference only.

```{eval-rst}
.. autoclass:: paxter.parse.CharLoc
   :members: line, col

.. autoclass:: paxter.parse.enclosing.EnclosingPattern
   :members: left, right

.. autoclass:: paxter.parse.enclosing.GlobalEnclosingPattern
   :members: left, right
   :show-inheritance:
```

## Evaluation

The following class implements the basic tree evaluation in Paxter language.
Users may want to extend this class to override the tree evaluation.

```{eval-rst}
.. autoclass:: paxter.evaluate.context.EvaluateContext
   :members:
```

The evaluated list of fragments will be of the following type

```{eval-rst}
.. autoclass:: paxter.evaluate.data.FragmentList
   :members:
   :show-inheritance:
```

### Function decorators

Wrappers for functions in python environments
to be used as function decorators.

```{eval-rst}
.. autoclass:: paxter.evaluate.wrappers.BaseApply

.. autoclass:: paxter.evaluate.wrappers.DirectApply
   :show-inheritance:

.. autoclass:: paxter.evaluate.wrappers.NormalApply
   :show-inheritance:

.. autoclass:: paxter.evaluate.wrappers.NormalApplyWithEnv
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
