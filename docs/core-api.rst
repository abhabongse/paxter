##################
Core API Reference
##################

Paxter language package provides the following core functionality.


Parsing
=======

The following class is where the main Paxter language parsing logic happens.

.. autoclass:: paxter.parse.ParseContext
   :members: input_text, tree


Data Definitions
----------------

Results of the Paxter language parsing yields parsed trees
which consist of instances of the following data classes.

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


Other Utility Classes
---------------------

Other classes related to parsing,
presented here for reference only.

.. autoclass:: paxter.parse.CharLoc
   :members: line, col

.. autoclass:: paxter.parse.enclosing.EnclosingPattern
   :members: left, right

.. autoclass:: paxter.parse.enclosing.GlobalEnclosingPattern
   :members: left, right
   :show-inheritance:

----


Evaluation
==========

The following class implements the basic tree evaluation in Paxter language.
Users may want to extend this class to override the tree evaluation.

.. autoclass:: paxter.evaluate.context.EvaluateContext
   :members:

The evaluated list of fragments will be of the following type

.. autoclass:: paxter.evaluate.data.FragmentList
   :members:
   :show-inheritance:


Function decorators
-------------------

Wrappers for functions in python environments
to be used as function decorators.

.. autoclass:: paxter.evaluate.wrappers.BaseApply

.. autoclass:: paxter.evaluate.wrappers.DirectApply
   :members: wrapped
   :show-inheritance:

.. autoclass:: paxter.evaluate.wrappers.NormalApply
   :members: wrapped
   :show-inheritance:

.. autoclass:: paxter.evaluate.wrappers.NormalApplyWithEnv
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
