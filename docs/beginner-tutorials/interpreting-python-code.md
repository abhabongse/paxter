# Interpreting Python Code

Let us assume that we are still using the environment dictionary created by
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
Learn more on Paxter’s ways to escape special characters on the page [](escaping-mechanisms.md).
:::


### Define New Functions

:::{admonition,caution} Under Construction
This entire page is under construction.
:::

(evaluating-python-expressions)=
## Evaluating Python Expressions

(disable-python-code-interpretation)=
## Disable Python Code Interpretation
