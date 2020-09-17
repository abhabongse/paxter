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

Nevertheless, a burning question remains:
what happens if our python source code itself contains a quotation mark?

:::{admonition,caution} Under Construction
This entire page is under construction.
:::

### Define New Functions

(evaluating-python-expressions)=
## Evaluating Python Expressions

(disable-python-code-interpretation)=
## Disable Python Code Interpretation
