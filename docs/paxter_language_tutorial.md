# Paxter Language Tutorial

```eval_rst
.. note:: 

   This is a tutorial for bare Paxter language,
   which discusses only the basic Paxter syntax without any semantics.
   The semantics to the parsed tree is generally given by users of Paxter library.
   For a simpler usage of Paxter, please also see
   :doc:`Python Authoring Mode Tutorial page<python_authoring_mode_tutorial>`.
```

Paxter syntax is very simple. 
In almost all cases, a typical text will be a valid Paxter document.
However, Paxter provides a special syntax to insert a richer data
into the document itself called an **@-expressions** (pronounced as “at expressions”).
There are 3 kinds of @-expressions:
**(1)** a command,
**(2)** a wrapped fragment list, and
**(3)** a wrapped text.


## Command

A **command** always begin with a switch, indicated by an **@**-symbol.
Following the switch, a command consists of 3 sections as follows.

```text
"@" introduction [options] [main argument]
```

Among these 3 sections, only the introduction section is mandatory;
the other 2 sections are optional and may be omitted.
There should _not_ be any whitespace characters separating between
the switch and the introduction section,
or between different sections of the same command.

### Introduction section

Any text could be part of an introduction section of a command.
There are 2 different ways to write down a command introduction section:
either **(a)** using an identifier form
or **(b)** surrounding the text with a _bar pattern_.

-   **(a)** If the text itself already has a valid Python identifier form
    (such as “foo”, “_create”, or even “จำนวน”),
    then you may simply write them down as is.
    For example,
    
    ```text
    @foo
    @_create
    @สวัสดี
    ```

-   **(b)** However, there are variety of texts that do not conform to 
    a Python identifier form.
    Hence, there is another way to write the introduction section:
    using a bar pattern.
    Simply surround the text with a pair of bars. 

    For example, if you wish to write “1 + 1” as introduction section of the command,
    you may write it as follows:
    
    ```text
    @|1 + 1|
    ```
    
    Sometimes, the text may contain a bar as part of itself (such as “left || right”).
    Then you may additionally surround the matching pair of bars
    with an equal number of hashes:
    
    ```text
    @#|left || right|#
    ```
    
    Obviously, if the introduction section begins with _n_ hashes followed by a bar,
    then the text itself may _not_ contain a bar followed by _n_ hashes.
    (Otherwise, the introduction section would have terminated earlier.)
    
    ```text
    @##|good|#|boy|##  →  the introduction section is "good|#|boy"
    @##|bad|##|boy|##  →  the introduction section is "bad"
    ```

### Options section

The existence of a left square bracket right after the introduction section
of a command always indicates the beginning of the options section.
The options section itself is a sequence of tokens where each token can be

-   Another @-expression of all 3 kinds
-   An identifier
-   An operator which can be a comma, a semicolon,
    or a combination of all other symbol characters
    (excluding parentheses, braces, and square brackets)
-   A number whose syntactical form adheres to JSON grammar for number literal
-   A nested sequence of tokens itself, surrounded by a matching pair of
    parentheses, braces, or square brackets.

```eval_rst
.. warning::

   Please note that inside the options section of a command
   is the only place in Paxter language where whitespace characters
   between tokens are ignored.

.. note::

   Consult :doc:`Syntax Reference <syntax>` for 
   a more detailed Paxter language grammar specification.
```

Here is an example of commands with options section present:

-   The options section of the command `@foo[x=1, y=2.5]`
    is a sequence of 7 tokens: 
    
    1.  an identifier `x`
    2.  an equal sign operator `=`
    3.  the number literal `1`
    4.  a comma operator `,`
    5.  an identifier `y`
    6.  an equal sign operator `=`, and
    7.  the number literal `2.5`

-   The options section of the command `@|foo.bar|[x <- {2}; @baz]`
    is a sequence of 5 tokens:
    
    1.  an identifier `x`
    2.  a left arrow operator `<-`
    3.  a nested sequence containing the number literal `2` as the only token
    4.  a semicolon operator `;`
    5.  a nested command with `baz` as the introduction section
        and with all other sections omitted.

Paxter language gives a lot of freedom for what is allowed
within the options section of a command;
a programmer-writer who writes a renderer to translate parsed trees in Paxter
is free to add whatever constraints to the formatting within the options section.

```eval_rst
.. note::

   As an example, the Python authoring mode renderer enforces that
   the options section must follow Python function call pattern,
   which is a sequence of positional arguments followed by
   a sequence of keyword arguments, each separated by commas
   (such as ``@replace[@"i", @"o", count=3]{Mississippi}``).
```

### Main argument section

There are two modes of main argument section:
**(a)** braces pattern mode and **(b)** quotation pattern mode.

```eval_rst
.. todo:: 

   More coming soon.
```
