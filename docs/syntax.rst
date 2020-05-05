Syntax Reference
================

Below are syntax diagrams for Paxter language. 

* **Document**: Top-level document; parsing starts here.
  Once all fragments of the fragment list is parsed,
  the caret pointer must end exactly at the end of input text.

  .. image:: _static/Document.png

  |nbsp|

* **FragmentList:** Consists of an interleaving of raw texts and @-commands,
  and ends with dynamically designated *break pattern*
  (which is simply tells where the fragment list stops).

  .. image:: _static/FragmentList.png

  |nbsp|

  For example, if preceding the fragment list is an opening brace pattern ``##<#{``,
  then the break (i.e. closing) pattern for this fragment list would be ``}#>##``,
  which mirrors the opening pattern.

  Please note that by construction of the language,
  the non-empty raw text would never contain the *break pattern*;
  if it was the case then the parsing of fragment list would have terminated earlier.
  In other words, we *non-greedily* parses text within the fragment list.

  The result of parsing fragment list is a :class:`FragmentList <paxter.core.FragmentList>` node type
  whose children is a list of :class:`Text <paxter.core.Text>` or command tokens.

  |nbsp|

* **Command:** Parses right after the @-symbol for one of 6 possibilities.

  .. image:: _static/Command.png

  |nbsp|

  .. note::

     The red ``else`` box in this diagram indicates that such path can be followed
     only if the next token does not match any other possible paths.
     Walking through the boxes in itself consumes nothing.

  .. note::

     The *prefix pattern* matched before the fragment list or the non-recursive text
     will be used to determine the break pattern indicating when to stop parsing for
     the fragment list or the non-recursive text itself, respectively.
     The break pattern is generally the mirror image of the matched prefix pattern,
     and can be computed by flipping the entire string as well as flipping
     each individual character to its mirror counterpart.

  Possible results are:

  * A :class:`PaxterApply <paxter.core.PaxterApply>` which consists of an identifier,
    followed by at least one option section or one main argument section.
    The option section is a list of tokens enclosed by a pair of square brackets
    (node is represented with :class:`TokenList <paxter.core.TokenList>`).
    On the other hand, the main argument section (surrounded by the dashed box in diagram below)
    is either a fragment list (represented with :class:`FragmentList <paxter.core.FragmentList>`)
    or a non-recursive raw text (represented with :class:`Text <paxter.core.Text>`).

  * However, if the token immediately succeeding the identifier
    neither does match the option section path nor does match the main argument path,
    the the parsing results in the identifier-style :class:`PaxterPhrase <paxter.core.PaxterPhrase>`
    whose inner phrase content derives from the identifier string.

  * If the command begins with the brace prefix pattern,
    then the parsing yields the :class:`FragmentList <paxter.core.FragmentList>` node as a result.

  * If the command begins with the quoted prefix pattern,
    then the parsing yields a regular :class:`Text <paxter.core.Text>` node as a result

  * If the command begins with the bar prefix pattern,
    then the parsing outputs the normal :class:`PaxterPhrase <paxter.core.PaxterPhrase>` node.

  * Finally, if the first token found does not match any of the above scenarios,
    then a single symbol codepoint is consumed and such character becomes
    the inner phrase content of symbol-style :class:`PaxterPhrase <paxter.core.PaxterPhrase>`.

  |nbsp|

* **TokenList:** A sequence of zero or more tokens
  Each token either a command, an identifier, an operator,
  a number following JSON specification,
  or a nested token list enclosed by a pair of parentheses ``()``,
  a pair of square brackets ``[]``, or a pair of pure braces ``{}``.
  The result is a :class:`TokenList <paxter.core.TokenList>` node type.

  .. image:: _static/TokenList.png

  |nbsp|

  .. note::

     The option section (or the token list) is the only place where whitespaces
     are ignored (when they appear between tokens).

  |nbsp|

* **Identifier:** Generally follows Python rules for parsing identifier token
  (with some exceptions).
  The result is an :class:`Identifier <paxter.core.Identifier>` node type.

  .. image:: _static/Identifier.png

  |nbsp|

* **Operator:** Greedily consumes as many operator character as possible
  (with two notable exceptions: a comma and a semicolon, which has to appear on their own).
  A whitespace may be needed to separate two consecutive, multi-character operator tokens.
  The result is an :class:`Operator <paxter.core.Operator>` node type.

  .. image:: _static/Operator.png

  |nbsp|

* **NonRecursiveText:** Parses the text content until encountering the *break pattern*.
  As opposed to fragment list, no @-symbol will be recognized
  as the indicator of the beginning of a command.

  Text extracted through this process will be used as the inner content of either
  :class:`Text <paxter.core.Text>` or :class:`FragmentList <paxter.core.FragmentList>`
  while a command is being parsed.

  .. image:: _static/NonRecursiveText.png

  |nbsp|

.. |nbsp| unicode:: 0xA0
   :trim: