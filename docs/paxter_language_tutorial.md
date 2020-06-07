# Paxter Language Tutorial

```eval_rst
.. note:: 

   This is a tutotrial for *bare* Paxter language specification.
   It discusses only the basic Paxter syntax without any associated semantics
   as the semantics to the intermediate parsed tree is generally given
   by users of Paxter library.

   For a simpler usage of Paxter library package, please also see
   :doc:`Python authoring mode tutorial page <python_authoring_mode_tutorial>`.
```

Paxter syntax is very simple.
In most cases, a typical text is a valid Paxter document, like in the following:

```text
Hello, World!
My name is Ashley, and I am 33 years old.
```

However, Paxter provides a special syntax called **@-expressions**
(pronounced as “at expressions”)
so that richer information may be inserted into the document.
There are 3 kinds of @-expressions, all of which begins with an @-symbol:

1. a text wrapped within the _quoted pattern_
2. a fragment list, wrapped within the _brace pattern_
3. a command (the most powerful syntax in Paxter)

This @-symbol is sometimes called a _switch_ because it indicates 
the beginning of an @-expression,
and whatever follows the switch determines which kind of @-expression it is.

Next, we dive into each kind of @-expressions.

```eval_rst
.. note::

   While reading on the next 2 sections on the first 2 kinds of @-expressions,
   it may not be obvious yet why they are imporant
   because all of the juicy meat is in the last kind of @-expressions, the command.

   So may I suggest readers to skim the next 2 sections, read on how the command works,
   then jump back to read those 2 sections again.
```


## 1. Wrapped Text 

An @-expression of this kind begins with an @-symbol,
then it is followed by a textual content wrapped within the _quoted pattern_,
which means that the inner text must be surrounded by 
a pair of quotation marks (U+0022).

So for example, here is a text `Hello, World!` written in wrapped text form:

```text
@"Hello, World!"
```

One important thing to note about the wrapped text is that
@-symbols contained within the inner content of the wrapped text
will _never_ be interpreted as a switch for @-expressions.
Hence, the usefulness of this kind of syntax shines best
when we would like to write something containing @-symbols (such as email)
since **there is no other mechanisms to escape @-symbol switches**.

In the example below, both are acceptable ways to “escape” @-symbols.
However, the first one will be parsed into simply a single token `ashley@example.com`
whereas the second one will be parsed into a sequence of 3 tokens:
`ashley`, `@`, and `example.com`.

```text
@"ashley@example.com"
ashley@"@"example.com
```

But what if we wish to include quotation marks within the inner content
of the wrapped text?
Luckily there is rather a non-painful way to write this:
simply append **an equal number of hashes** (U+0023) to 
_both ends_ of the matching quotation mark pairs.

Confused? Let’s consider the following example.

```text
@"No "quotation marks" allowed here."
@##"Allowing "quotation marks" within the wrapped text."##
```

For the first line, the second quotation mark preceding the word _quotation_
is matched with the very first quotation mark right after the beginning @-symbol.
Hence, the inner content of the first wrapped text is simply `No `
(with a space at the end),
followed by `quotation marks" allowed here."` as the second text token
(**not** `No "quotation marks" allowed here.` as some might have expected).

However, the whole sentence in the second line of the above example
constitutes the entire inner content of the wrapped text.
Note that if the sentence itself were to contain `"##` somewhere mid-sentence,
then the parsing of the wrapped text would have terminated earlier.

In the next example below, 
the first line of input is parsed into a single token `good"#"boy`
whereas the second line is parsed into two tokens, `bad` and `"boy"##`.
 
```text
@##"good"#"boy"##
@##"bad"##"boy"##
```

```eval_rst
.. important::

   An important thing to remember is that Paxter parser will attempt to
   *non-greedily* match the **balanced pair of hashes for the quoted pattern**.
   In fact, this also applies to other kinds of patterns, which we will see later.
```


## 2. Wrapped Fragment List

Wrapped fragment lists differs from wrapped texts for 2 major reasons:

-   Instead of using a pair of quotation marks surrounding the inner content, 
    wrapped fragment lists uses a matching pair of braces instead
    (U+007B and U+007D).
    This is called the _brace pattern_ in analogous to the _quoted pattern_
    for wrapped texts.
-   Nested @-expressions are allowed within the inner content of wrapped fragment lists.
    
This kind of @-expressions will be proven useful when we wish to embed textual data
within the options section of a command (to be discussed below).

Below is one example of how this kind of syntax is used.
Do not worry about the unfamiliar command syntax yet,
just know that the area between the matching pair of square brackets 
is called the _options section_ of a command.

```text
@ordered_list[
    @{This is the first item},
    @{This is the second item},
    @{Send your complaints to my email at @"ashley@example.com"!},
]
```


## 3. Command

A **command** is the most powerful syntax in Paxter language.
It consists of the following 3 sections of information:

```text
"@" introduction [options] [main_argument]
```




## 1. Command

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
or **(b)** surrounding the text with the _bar pattern_.

-   **(a)** If the text itself already has a valid Python identifier form
    (such as `foo`, `_create`, or even `จำนวน`),
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
    using the _bar pattern_.
    Simply surround the text with a pair of bars. 

    For example, if you wish to write `1 + 1` as introduction section of the command,
    you may write it as follows:
    
    ```text
    @|1 + 1|
    ```
    
    Sometimes, the text may contain a bar as part of itself (such as `left || right`).
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

### Main argument section

Main argument section, if exists, contains the main text associated to a command.
There are 2 modes for the main argument section:
**(a)** wrapped fragment list mode and **(b)** wrapped raw text mode.

-   **(a)** For a fragment list mode as the main argument,
    the text content is allowed to be mixed with nested @-expressions.
    
    The main argument content of this mode must be surrounded by a pair of braces
    (called the _brace pattern_, which is analogous to the _bar pattern_).
    For example,
    
    ```text
    @foo{Hello, @name}.
    ```
    
    If the main argument has to contain right braces,
    then the pair of matching braces may additionally surrounded by
    the same number of hashes, as in the following:
    
    ```text
    @foo##{A set of natural numbers {0, 1, 2, ...}.}##
    ```
    
    Similarly to the _bar pattern_ from the introduction section,
    if the wrapped fragment list begins with _n_ hashes followed by a left brace,
    then the _immediate_ inner content may not contain
    a right brace followed by _n_ hashes. 
    
    For example, the following piece of Paxter document
    is a command with `foo` as the introduction,
    and with `@bar{1}###@bar{2}` as the main argument.
    Notice that the right brace right after `1` is not associated
    with the succeeding `###` because it matches with the left brace
    preceding `1`.
    ```text
    @foo###{@bar{1}###@bar{2}}###
    ```
    
-   **(b)** For a wrapped text mode as the main argument,
    nested @-symbols will _not_ be interpreted as the switch for @-expressions.
    And instead of using a matching pair of braces, 
    a pair of straight quotation mark has to be deployed.
    This is called the _quoted pattern_.
    
    This is useful especially when you expect the content 
    of the main argument to be from another domain where @-symbol is prevalent.
    For example, 
    ```text
    @mailto"yourname@example.com"
    ```
    
    Again, if the inner text needs to contain a quotation mark,
    add an equal number of hashes to both ends.
    
    ```text
    @alert#"Send your feedback to "yourname@example.com"."#
    ```

### Combinations

Obviously, both the options section and the main argument section
may be presented at the same time. For example,

```text
@repeat[15]{I will submit my homework on time next time! }
```

### Special form

There is a special form of a command, which is when there is 
a single symbol character that follows the @-switch.
Such symbol will become the sole content of the introduction section,
while the options section and the main argument section are considered empty.

For example, both lines presented below are considered identical.

```text
Email from me@@example.com: stop by today between 3@,-@,5 PM.
Email from me@|@|example.com: stop by today between 3@|,|-@|,|5 PM.
```
