# Paxter Language Tutorial

```{eval-rst}
.. todo::

   This page requires revision.

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
(pronounced “at expressions”)
so that richer information may be inserted into the document.
There are 2 kinds of @-expressions, all of which begins with an @-symbol:
a command and a short symbol expression.

This @-symbol (codepoint U+0040) is sometimes called a _switch_ 
because it indicates the beginning of an @-expression,
and whatever follows the switch determines which kind of @-expression it is.

Next, we dive into each kind of @-expressions.

```{eval-rst}
.. note::

   Consult :doc:`Syntax Reference <../references/syntax>` for 
   a more detailed Paxter language grammar specification.
```


## 1. Command

A **command** is the most powerful syntax in Paxter language.
It consists of the following 3 sections of information:

```text
"@" starter [option] [main_argument]
```

Among these 3 sections, only the starter section is mandatory;
the other 2 sections are optional and can be omitted.
Additionally, there should _not_ be any whitespace characters
separating between the switch and the starter section,
nor between different sections of the same command.

### Starter section

A starter of a command may contain any textual content,
surrounded by a pair of bars `|` (U+007C).

Here are examples of a valid command with only the starter section.

```text
@|foo|
@|_create|
@|สวัสดี|
@|foo.bar|
@|1 + 1|
@|Hello, World!|
```

However, if the content of the starter section
takes the form of a valid Python identifier,
then the pair of bars may be dropped. 
So the first 3 examples from above may be rewritten as follows:

```text
@foo
@_create
@สวัสดี
```

On the other hand, the textual content of the starter may sometimes 
contain a bar as part of itself (such as `x || y || z`).
Then we may additionally surround the matching pair of bars
with an equal number of hashes `#` (U+0023):

```text
@#|x || y || z|#
@###|x || y || z|###
```

But the following example will _not_ work as expected:

```text
@|x || y || z| is a command whose starter content contains exactly just “x ”
followed by regular text “| y || z|”.
```

Obviously, if the starter section begins with _n_ hashes followed by a bar,
then the textual content itself _cannot_ contain a bar followed by _n_ or more hashes
(otherwise, the starter section would have terminated earlier).

```text
@##|good|#|one|##
@##|bad|##|one|##
```

In this example (shown above), the starter of the first command is `good|#|boy`
whereas that of the other command cuts short at `bad`
(followed by the text `|one|##`).

**Note:** In a sense, this _bar pattern_ (by which we mean 
the pattern of surrounding some content with a pair of bars
plus an equal number of hashes on both ends) will be parsed **non-greedily**
(i.e. the parsing of the starter halts as soon as the closing pattern
corresponding to the opening pattern encountered earlier is found).

### Main argument section

Let’s skip the option section for now 
and discuss the main argument section of a command first.

As the name suggests, the main argument section of a command
contains the most important piece of information to which the command is applied.
The main argument can be supplied in one of 2 modes:
the fragment list mode (in which the content is wrapped within the _brace pattern_)
and the text mode (i.e. the content is wrapped within the _quoted pattern_).

#### (a) Wrapped fragment list mode

For a fragment list mode as the main argument,
the content may contain texts as well as any _nested_ @-expressions.

The content itself must be surrounded by a pair of curly braces
(U+007B and U+007D) called the _brace pattern_
(in analogous to the _bar pattern_ associated with the starter section of a command).
Of course, additionally appending the equal number of hashes to both ends are allowed.

For example,

```text
@foo{Hello, @name}
@|font.large|{BUY ONE GET ONE FREE!}
@highlight##{A set of natural numbers: {0, 1, 2, 3, ...}.}##.
```

Similarly to the _bar pattern_ from the starter section of a command,
if the wrapped fragment list begins with _n_ hashes followed by a left curly brace,
then the **immediate** inner textual content may _not_ contain
a right curly brace followed by _n_ or more hashes.

In the following example, the outermost command has the starter `foo`
and its main argument is in fact `@bar{1###}###`.
That is because (1) the curly braces pair surrounding `1###`
(marked with “^”) match with each other, 
and thus (2) the succeeding 3 hashes are not associated 
with the marked closing curly brace.  

```text
@foo###{@bar{1###}###}###
            ^    ^
```

#### (b) Wrapped text mode

Wrapped texts are somewhat similar to wrapped fragment lists,
except for 2 major aspects:

-   Instead of using a matching pair of curly braces surrounding the inner content,
    wrapped texts use a pair of quotation marks (U+0022).
    This is called the _quoted pattern_ in analogous to the _brace pattern_
    for wrapped fragment lists.
-   All @-symbol characters within the textual content
    will _not_ be interpreted as the switch for @-expressions.
    Hence, wrapped texts would _not_ contain any nested @-expressions.

This mode of main argument is useful especially when we expect the inner content
of the main argument to be from **another domain** where @-symbols are prevalent.

For example, when you want to embed source code from another language:

```text
@python_highlight##"

    # Results of the following function is cached 
    # depending on its input
    from functools import lru_cache
    
    @lru_cache(maxsize=None)
    def add(x, y):
        """Adding function with caching."""
        return x + y

"##
```

Again, if the inner content needs to contain a quotation mark,
we may add an equal number of hashes to both ends:

```text
@alert#"Submit your feedback to "ashley@example.com"."#
```

### Option section

The existence of a left square bracket immediately after the starter section
of a command _always_ indicates the beginning of the option section.
The option section itself is a sequence of _tokens_ where each token can be
one of the following:

-   **Another @-expression** of any kind
-   **An identifier** (according to Python grammar)
-   **An operator** which can be a single comma, a single semicolon,
    or a combination of all _other_ symbol characters
    (excluding hashes, quotation marks, curly braces, and square brackets)
-   **A number** whose syntactical form adheres to JSON grammar for number literal
-   **A fragment list** wrapped within the _brace pattern_
    (which shares the same syntax as already discussed in the main argument section)
-   **A text** wrapped within the _quoted pattern_
    (which shares the same syntax as already discussed in the main argument section)
-   **A nested sequence of tokens** itself,
    surrounded by a matching pair of square brackets (U+005B and U+005D).

```{eval-rst}
.. warning::

   Please note that inside the option section of a command
   is the only place in Paxter language where whitespace characters
   between tokens are ignored.
```

Here are a couple of examples of commands which include the option section:

-   For the command `@foo[x="bar", y=2.5, z={me}]{text}`,
    its option section contains a sequence of 11 tokens:
    
    1.  an identifier `x`
    2.  an equal sign operator `=`
    3.  a text token `bar`
    4.  a comma operator `,`
    5.  an identifier `y`
    6.  an equal sign operator `=`
    7.  the number literal `2.5`
    8.  a comma operator `,`
    9.  an identifier `z`
    10. an equal sign operator `=`, and
    11. a fragment list containing the text `me`

-   For the command `@|foo.bar|[x <- [2]; @baz]`,
    its option section contains a sequence of 5 tokens:
    
    1.  an identifier `x`
    2.  a left arrow operator `<-`
    3.  a nested sequence containing the number literal `2` as the only token within it
    4.  a semicolon operator `;`, and
    5.  a nested command with `baz` as the starter section
        and with all other sections omitted.

Paxter language syntax gives a lot of freedom for what is allowed within
the option section of a command;
a programmer-write who writes a renderer to transform Paxter intermediate parsed trees
into data of another form has a liberty to add whatever constraints
to the syntactical structure within the option section.


## 2. Single Symbol Expression

This kind of @-expression is in the form of a single symbol character
immediately following the @-symbol switch.
This single _symbol_ character will be the sole content
of the single symbol expression.

For example,

```text
There is free food today between 3@,-@,5 PM.
```

```{eval-rst}
.. warning::

   If ``@#`` happens to be the prefix of a full-form @-expressions
   (such as in ``@#|foo|#``),
   then ``@#`` by itself is *not* a valid command in special form.
   It must be **unambiguously** *not* part of full-form command
   for itself to become a valid command of special form.
```


## Escaping @-Symbol Switches

Paxter language does _not_ provide any syntax to escape
@-symbol switches of @-expressions.
We recommend the library user solve this kind of problem
at the interpreter/renderer level instead.

One way to do this is to define the behavior of `@@`
(a single symbol expression with `@` symbol following the switch)
to be transformed into a single `@` symbol in the rendered output.

```text
My email is ashley@@example.com.
```

Another method to work around this problem is to introduce
a command called `verbatim` (inspired by the command of the same name in LaTeX) 
which will output the main input argument as-is.

```text
My email is @verbatim"ashley@example.com".
```
