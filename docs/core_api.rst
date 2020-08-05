##################
Core API Reference
##################

Paxter language package provides the following core functionality.

Exceptions
==========

These are all the exception classes raised from this library package.

.. autoclass:: paxter.exceptions.PaxterBaseException
   :members: message, positions
   :show-inheritance:

.. autoclass:: paxter.exceptions.PaxterConfigError
   :show-inheritance:

.. autoclass:: paxter.exceptions.PaxterSyntaxError
   :show-inheritance:

.. autoclass:: paxter.exceptions.PaxterRenderError
   :show-inheritance:

----


Parsing
=======

The following class is where the main Paxter language parsing logic happens.

.. autoclass:: paxter.parser.ParseContext
   :members: input_text, tree


Data Definitions
----------------

Results of the Paxter language parsing yields parsed trees
which consist of instances of the following data classes.

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
   :members: children, enclosing
   :show-inheritance:

.. autoclass:: paxter.parser.Text
   :members: inner, enclosing
   :show-inheritance:

.. autoclass:: paxter.parser.Command
   :members: starter, starter_enclosing, option, main_arg
   :show-inheritance:


Other Utility Classes
---------------------

Other classes related to parsing,
presented here for reference only.

.. autoclass:: paxter.parser.CharLoc
   :members: line, col

.. autoclass:: paxter.parser.EnclosingPattern
   :members: left, right

.. autoclass:: paxter.parser.GlobalEnclosingPattern
   :members: left, right

----


Evaluation
==========

The following class implements the basic tree evaluation in Paxter language.
Users may want to extend this class to customize the tree evaluation.

.. autoclass:: paxter.evaluator.EvaluateContext
   :members:


Function decorators
-------------------

Wrappers for functions in python environments
to be used as function decorators.

.. autoclass:: paxter.evaluator.BaseApply

.. autoclass:: paxter.evaluator.DirectApply
   :members: wrapped

.. autoclass:: paxter.evaluator.NormalApply
   :members: wrapped

.. autoclass:: paxter.evaluator.NormalApplyWithEnv
   :members: wrapped
