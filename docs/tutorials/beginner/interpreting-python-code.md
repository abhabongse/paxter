# Interpreting Python Code

Let’s assume that we are still using the environment dictionary created by
{func}`create_document_env() <paxter.author.environ.create_document_env>`
_together_ with the default interpreter, which is implemented by
{class}`InterpreterContext <paxter.interpret.context.InterpreterContext>`.
Under this particular setup,
there are various ways to embed and run python code within the source text itself.
We discuss each possibility below.

(executing-python-statements)=
## Executing Python Statements

It would seem at first that there is no way to introduce a new binding
from a phrase to a python object into the environment dictionary
on an ad-hoc basis (i.e. from within the source text).
Actually, we can do so through the `@python"..."` command,
by putting actual python statements in-between the pair of quotation marks.

### Assigning Variables

Here is one example where a long string is pre-defined once,
and reused multiple times.

```paxter
@python"yaa = 'Yet Another Acronym'"
YAA is @yaa and it stands for @yaa.
```

```html
<p>YAA is Yet Another Acronym and it stands for Yet Another Acronym.</p>
```

The command phrase `@python` maps to the callable object
{func}`python_unsafe_exec() <paxter.author.standards.python_unsafe_exec>`.
What this particular function does is executing the entire python source
through the built-in {func}`exec` function,
using the environment dictionary `env` as the global namespace.
When the assignment statement `yaa = 'Yet Another Acronym'` gets executed,
then the entry `env['yaa']` gets populated with the string `"Yet Another Acronym"`,
which is why the command `@yaa` can subsequently be referred to
within the source text.

Yet, a burning question arises:
what happens if the python source code itself has to contain quotation mark characters
when we also use it to delimit the main argument part of the `@python` command itself?
Let’s try that out!

```paxter
@python"yaa = "Yet Another Acronym""
YAA is @yaa and it stands for @yaa.
```

Attempting to evaluate the above source text yields the following error (omitting traceback for clarity):

```pytb
Traceback (most recent call last):
  ...
  File "<string>", line 1
    yaa = 
         ^
SyntaxError: invalid syntax

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  ...
paxter.exceptions.PaxterRenderError: paxter apply evaluation error at line 1 col 2
```

The reason behind this error is that the main argument part of the command
was prematurely terminated at the first (closing) quotation mark character it finds.
Therefore, the incomplete python statement `yaa = ` was parsed,
which yields the above error when executed.

The solution around this problem is to additionally enclose the quoted main argument
with **an equal number of hash characters** to both ends of the quoted argument.
For example, in the source text below,
the python source code begins at `#"` and ends at `"#`
(though we can also use the `##"`, `"##` pair as well).

```paxter
@python#"yaa = "Yet Another Acronym""#
YAA is @yaa and it stands for @yaa.
```

:::{admonition,tip} More Information
The **hash-enclosing rule** is enforced by the core Paxter language specification,
and it applies at other locations as well.
Learn more on Paxter’s ways to escape special characters on the page [](escaping-mechanisms.md).
:::


### Define New Functions

Continuing on the same line of thinking from above,
we could also define python functions using `@python` command
and make calls to them using command syntax from within the source text.

For example, we will create a new function that will repeat the main argument a few times.

```paxter
@python##"
def repeat(main_arg, n=2):
    return n * main_arg
"##

@repeat{woof}

@repeat[3]{@bold{hi}}

@repeat[n=4]{@repeat{?}!}
```

```html
<p>woofwoof</p>
<p><b>hi</b><b>hi</b><b>hi</b></p>
<p>??!??!??!??!</p>
```


### Using Imported Values and Functions

We can also use command syntax to refer to values and functions
obtained through the import statement.

```paxter
@python##"
from string import ascii_uppercase
from textwrap import shorten
"##

Letters in English alphabet are @ascii_uppercase.

@shorten[15]#"Good morning world!"#

@shorten["Good evening everyone.", width=20]
```

```html
<p>Letters in English alphabet are ABCDEFGHIJKLMNOPQRSTUVWXYZ.</p>
<p>Good [...]</p>
<p>Good evening [...]</p>
```

:::{admonition,important} Did you spot something?
Readers with a pair of eagle eyes will be able to spot that
we are liberally using the hash-enclosing rule here at the first `@shorten` command as well,
albeit totally unnecessary.
This is to illustrate that this hash-enclosing rule
works for _any_ command (not just `@python`).
:::


(evaluating-python-expressions)=
## Evaluating Python Expressions

Applying all of the knowledge we have learned so far with Paxter library,
one way to evaluate a python expression and print its result inside the source text
is to do the following two steps:

1. Inside the `@python` command, evaluate the desired expression and assign its result to a variable.
2. Refer to the value of such variable through the command syntax.

Here is an example to demonstrate the above process.

```paxter
@python##"
def add_one(value):
    return value + 1

ninetynine_plus_one = add_one(99)
product = 7 * 11 * 13
"##

The result of 99 + 1 is @ninetynine_plus_one.

The result of 7 * 11 * 13 is @product.
```

```html
<p>The result of 99 + 1 is 100.</p>
<p>The result of 7 * 11 * 13 is 1001.</p>
```

Fortunately, there is a much nicer way to evaluate an anonymous python expression
and insert its evaluation result right at _that_ location:
by using the `@|...|` syntax,
replacing `...` with the expression itself.

```paxter
@python##"
def add_one(value):
    return value + 1
"##

The result of 99 + 1 is @|add_one(99)|.

The result of 7 * 11 * 13 is @|7 * 11 * 13|.
```

```html
<p>The result of 99 + 1 is 100.</p>
<p>The result of 7 * 11 * 13 is 1001.</p>
```

Although this new syntax `@|...|` may seem new,
it is actually an alternative form of the **same old syntax command** with the same old semantics.
Here are some key points about this syntax and the command syntax in general.

- `@|...|` is still considered a command in Paxter language
  (no different from other commands we have seen so far up until this point).
  For this particular syntax, 
  **everything between the pair of bars is the phrase part of the command**.
  In fact, the command syntax `@foo` is the short form of `@|foo|` (both are syntactically equivalent).
  This realization also applies to commands with options part and/or main argument part.
  For example, `@foo[bar]{baz}` can also be written in full form as `@|foo|[bar]{baz}`.
  Conversely, one may say that the phrase part may be written _without the bars_
  if the entire phrase string resembles a python identifier form.
- Do you remember the section {ref}`interpreting-a-command` from a previous page
  where we discuss how a command is being interpreted?
  The very first step is to **resolve the phrase part**.
  Notice that as part of the {ref}`the backup plan <phrase-part-fallback-plan>`,
  the entire phrase will be evaluated as a python expression.
  This is why commands like `@|add_one(99)|` and `@|7 * 11 * 13|`
  work the way it is.

Let’s look at another example in which a command has a function call form
but the callable object is not stored inside a simple python identifier.

```paxter
@python##"
import string, textwrap
"##

Letters in English alphabet are @|string.ascii_uppercase|.

@|textwrap.shorten|[15]#"Good morning world!"#

@|textwrap.shorten|["Good evening everyone.", width=20]
```

```html
<p>Letters in English alphabet are ABCDEFGHIJKLMNOPQRSTUVWXYZ.</p>
<p>Good [...]</p>
<p>Good evening [...]</p>
```

And below is another example of rather complicated usage of the command syntax
(some concepts appeared below have not yet been discussed).

```paxter
@python##"
import statistics
d6_faces = [1, 2, 3, 4, 5, 6]
"##

The expected outcome of rolling a D6 is @|statistics.mean|[@d6_faces].
If we remove the first item from the list (which is @|d6_faces.pop|[0])
then we are left with @|' '.join|[@map[@str, @d6_faces]].
```

```html
<p>The expected outcome of rolling a D6 is 3.5.
   If we remove the first item from the list (which is 1)
   then we are left with 2 3 4 5 6.</p>
```

Before we move on, there is one more issue to address:
if the phrase part of a command could just be any python expression,
then how do we write expressions that contain bar characters themselves
(e.g. doing the bitwise or operation and the set union operation)?
Note that this kind of problem is very similar the previous problem (discussed earlier on this page)
where it was tricky to include quotation mark characters within quoted main argument, remember?

Paxter decides to solve all of these problem in the same way,
again, through hash-enclosing rule.
For example,

```paxter
The bitwise OR between 5 and 9 is @##|5 | 9|##.

The union of set {1, 2, 4, 8} and {2, 3, 5, 7} is @#|{1, 2, 4, 8} | {2, 3, 5, 7}|#.
```

```html
<p>The bitwise OR between 5 and 9 is 13.</p>
<p>The union of set {1, 2, 4, 8} and {2, 3, 5, 7} is {1, 2, 3, 4, 5, 7, 8}.</p>
```
