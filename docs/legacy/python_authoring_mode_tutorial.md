# Python Authoring Mode Tutorial

```eval_rst
.. todo::

   This page requires revision.
```

## Block Python Code Execution

In Python authoring mode,
Python source code may be embedded into the document for execution
using `python` command syntax with the code as the main argument.
For example,

```text
@python##"
    name = "Ashley"
"##
```

In the example document above, once the Python code in the preamble is executed,
the value of the variable `name` will be available in the environment
for the rest of the document. 

### Referring to variable from Python code

One way to referring to the value of the variable `name`
is to use the command syntax `@name` without any options or main arguments sections.
So the following document

```text
@python##"
    name = "Ashley"
"##
Hi, @name.
```

will be rendered into 

```text
 
Hi, Ashley.
``` 

### Remove unwanted newlines

Notice how the newline character was preserved in the above output.
If we wish to remove that newline character,
we may put a backslash at the end of that line.
So the following document

```text
@python##"
    name = "Ashley"
"##\
Hi, @name.
```

yields the following output in Python authoring mode

```text
Hi, Ashley.
```

### Referring to functions from Python code

We may also define Python functions within the embedded Python source code
and refer to them later in the document. 
The syntax to make a call to a function already defined
is a command syntax with the main argument supplied.
Here is one example,

```text
@python##"
    def surround(text):
        return "(" + flatten(text) + ")"
"##\
This is @surround{sound}.
```

which will return

```text
This is (sound).
```

The reason why we need to `flatten` the main argument first is that
the fragment list (i.e. the part surrounded by a matching pair of curly braces)
returns a list of string tokens (not the string itself),
hence it is important to flatten them into a single string first
(otherwise an error would have occurred).

### Python functions with multiple arguments

When there is more than one argument to the function,
the main argument of the command will always be the first argument of the function,
and the rest of the function arguments can be supplied
to option section of the command (similarly to Python function call syntax):

```text
@python##"
    def surround(text, n, left='(', right=')'):
        return flatten(left) * n + flatten(text) + flatten(right) * n
"##\
This is @surround[3]{sound}.
This is @surround[n=3]{sound}.
This is @surround[3, "[", "]"]{sound}.
This is @surround[3, right=""]{sound}.
This is @surround[n=3, left="_", right="_"]{sound}.
```

Here is the result.

```text
This is (((sound))).
This is (((sound))).
This is [[[sound]]].
This is (((sound.
This is ___sound___.
```

Notice that we use wrapped text inside the option section
in order to supply strings as arguments to the function `surround`.

Additionally, we may also omit the main argument section,
and then the entire option section will all be the arguments to the function:

```text
@python##"
    def surround(text, n, left='(', right=')'):
        return flatten(left) * n + flatten(text) + flatten(right) * n
"##\
This is @surround["sound",3].
This is @surround["sound",n=3].
```

The above document will be rendered into

```text
This is (((sound))).
This is (((sound))).
```


## Inline Python Code Evaluation

We may wish to insert the result of the evaluation of Python expression.
We can do so by using the command syntax with the bar pattern `@|...|`:

```text
The result of 7 × 11 × 13 is @|7 * 11 * 13|.
```

and that would be transformed into

```text
The result of 7 × 11 × 13 is 1001.
```

### Inline Python code with function call

If a function behind an attribute or key lookup,
we may use the bar pattern in conjunction with main arguments and/or options.

```text
@python##"
    import statistics
    values = [2, 3, 5, 7]
    funcs = {
        'median': statistics.median
    }
"##\
The average of first 4 primes is @|statistics.mean|[@values].
The median of first 4 primes is @|funcs['median']|[@values].
```

The above document returns the following.

```text
The average of first 4 primes is 4.25.
The median of first 4 primes is 4.0.
```


## Special Symbol Commands

For the sake of simplicity,
we provide an easy way to perform text replacements for symbol-style commands.
Simply define a dictionary mapping from each symbol to the substituting results
under the variable `_symbol_` inside the Python source code.

```text
@python##"
    _symbols_ = {
        '.': '&hairsp;',
        ',': '&thinsp;',
        '@': '@',
    }
"##\
My email is ashley@@example.com.
My office hours is between 7@.-@.9 PM.
```

Here is the result of the above document.

```text
My email is ashley@example.com.
My office hours is between 7&hairsp;-&hairsp;9 PM.
```


## Special Commands: For and If

For statements within the document for Python authoring mode
has the following format

```text
@for[<IDENTIFIER> in <EXPRESSION>]{<BODY>}
```

whereas if statements has the 3 following formats

```text
@if[<CONDITIONAL>]{<BODY>}
@if[not <CONDITIONAL>]{<BODY>}
@if[<CONDITIONAL> then <THEN_BODY> else <ELSE_BODY>]
```

Here is the document that illustrates how to use these special commands:

```text
@python##"
    def is_odd(value):
        return value % 2 == 1
"##\
Odd digits are @flatten{@for[i in @|range(10)|]{@if[@|is_odd(i)|]{ @i}}}.
Even digits are @flatten{@for[i in @|range(10)|]{@if[not @|is_odd(i)|]{ @i}}}.
Digits are @flatten{@for[i in @|range(10)|]{@if[@|is_odd(i)| then " odd" else " even"]}} in this order.
```

and the result would be

```text
Odd digits are 1 3 5 7 9.
Even digits are 0 2 4 6 8.
Digits are  even odd even odd even odd even odd even odd in this order.
```
