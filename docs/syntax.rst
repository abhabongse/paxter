Syntax Reference
================

Below are syntax diagrams for Paxter language. 

- **Document:** Starting rule of Paxter language grammar.
  It is a special case of **FragmentList** rule, and thus
  the result is always a :class:`FragmentList <paxter.core.FragmentList>` node
  whose children are non-empty :class:`Text <paxter.core.Text>`
  interleaving with the result produced by **AtExpression** rule.

  .. image:: _static/Document.png

  |nbsp|

- **AtExpression:** Rule for parsing right after encountering @-switch symbol.

  .. image:: _static/AtExpression.png

  |nbsp|

  .. note::

     The red ``else`` box in this diagram indicates that such path can be followed
     only if the next token does not match any other possible paths.
     Pursuing this ``else`` path does not consume anything.

  There are 2 possible scenarios.

  1. A normal :class:`Command <paxter.core.Command>` node consisting of 3 sections:
     starter, options, and main argument, respectively.

     The starter section is resulted from parsing
     either greedily for an identifier or non-greedily for a text
     enclosed by a pair of bars plus and an equal number of zero or more hashes
     at both ends.

     Following the starter section, if a left square bracket is found,
     then the option section as a list of tokens must be parsed
     and it will result in a :class:`TokenList <paxter.core.TokenList>` node.
     Otherwise (if the left square bracket is absent),
     this option section will be represented by :const:`None`.

     Finally, the main argument section.
     (a) If there is zero or more hashes followed by a left brace,
     then the **FragmentList** parse rule must be followed
     and thus yields :class:`FragmentList <paxter.core.FragmentList>` as the result.

     .. warning::

        There is a restriction imposed on parsing the **FragmentList** rule,
        which is that the child text node may not contain a right brace
        followed by the same number of hashes as the preceding part.
        Otherwise, the parsing of **FragmentList** rule would have terminated earlier.

     However, (b) if there is zero or more hashes followed by a quotation mark,
     then the text is parsed non-greedily until the another quotation mark
     followed by the same number of hashes is found.

     Well, if both conditions (a) and (b) do not hold,
     then the main argument would be :const:`None`.

  2. A special :class:`SingleSymbol <paxter.core.SingleSymbol>` node where
     a single symbol follows the @-switch.

- **FragmentList:** Consists of an interleaving of non-empty texts
  and results produced by **AtExpression** rule.

  Note that the parsing of **AtExpression** rule at the *previous level*
  may put some restriction on the parsing of :class:`Text <paxter.core.Text>` nodes.
  For example, if preceding the fragment list is an opening brace pattern ``###{``,
  then each :class:`Text <paxter.core.Text>` node may contain ``}###``.

  In other words, we *non-greedily* parses text within the fragment list.

  .. image:: _static/FragmentList.png

  |nbsp|

- **TokenList:** A sequence of zero or more tokens
  Each token either a command, an identifier, an operator,
  a number following JSON specification,
  a wrapped fragment list, a wrapped text,
  or a nested token list enclosed by a pair of square brackets ``[]``.
  The result is a :class:`TokenList <paxter.core.TokenList>` node type.

  .. image:: _static/TokenList.png

  |nbsp|

  .. note::

     The option section (or the token list) is the only place where whitespaces
     are ignored (when they appear between tokens).

  |nbsp|

- **Identifier:** Generally follows Python rules for greedily parsing
  an identifier token (with some extreme exceptions).
  The result is an :class:`Identifier <paxter.core.Identifier>` node type.

  .. image:: _static/Identifier.png

  |nbsp|

- **Operator:** Greedily consumes as many operator character as possible
  (with two notable exceptions: a comma and a semicolon, which has to appear on their own).
  A whitespace may be needed to separate two consecutive, multi-character operator tokens.
  The result is an :class:`Operator <paxter.core.Operator>` node type.

  .. image:: _static/Operator.png

  |nbsp|

.. |nbsp| unicode:: 0xA0
   :trim:
