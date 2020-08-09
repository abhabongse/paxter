##################
Core API Reference
##################

Paxter language package provides the following core functionality.


Parsing
=======

The following class is where the main Paxter language parsing logic happens.

.. autoclass:: paxter.parser.ParseContext
   :members: input_text, tree


Data Definitions
----------------

Results of the Paxter language parsing yields parsed trees
which consist of instances of the following data classes.

.. autoclass:: paxter.parser.data.Token
   :members: start_pos, end_pos
 
.. autoclass:: paxter.parser.data.Fragment
   :show-inheritance:

.. autoclass:: paxter.parser.data.TokenSeq
   :members: children
   :show-inheritance:

.. autoclass:: paxter.parser.data.Identifier
   :members: name
   :show-inheritance:

.. autoclass:: paxter.parser.data.Operator
   :members: symbols
   :show-inheritance:

.. autoclass:: paxter.parser.data.Number
   :members: value
   :show-inheritance:

.. autoclass:: paxter.parser.data.FragmentSeq
   :members: children, enclosing
   :show-inheritance:

.. autoclass:: paxter.parser.data.Text
   :members: inner, enclosing
   :show-inheritance:

.. autoclass:: paxter.parser.data.Command
   :members: phrase, phrase_enclosing, options, main_arg
   :show-inheritance:


Other Utility Classes
---------------------

Other classes related to parsing,
presented here for reference only.

.. autoclass:: paxter.parser.CharLoc
   :members: line, col

.. autoclass:: paxter.parser.enclosing.EnclosingPattern
   :members: left, right

.. autoclass:: paxter.parser.enclosing.GlobalEnclosingPattern
   :members: left, right
   :show-inheritance:

----


Evaluation
==========

The following class implements the basic tree evaluation in Paxter language.
Users may want to extend this class to override the tree evaluation.

.. autoclass:: paxter.evaluator.context.EvaluateContext
   :members:

The evaluated list of fragments will be of the following type

.. autoclass:: paxter.evaluator.data.Fragments
   :members:
   :show-inheritance:


Function decorators
-------------------

Wrappers for functions in python environments
to be used as function decorators.

.. autoclass:: paxter.evaluator.wrappers.BaseApply

.. autoclass:: paxter.evaluator.wrappers.DirectApply
   :members: wrapped
   :show-inheritance:

.. autoclass:: paxter.evaluator.wrappers.NormalApply
   :members: wrapped
   :show-inheritance:

.. autoclass:: paxter.evaluator.wrappers.NormalApplyWithEnv
   :members: wrapped
   :show-inheritance:

----


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
