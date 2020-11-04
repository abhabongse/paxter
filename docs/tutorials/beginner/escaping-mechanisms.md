# Escaping Mechanisms

Upon tinkering with writing blog posts through {mod}`paxter.author` subpackage,
we would eventually find out some technical limitations
with the command syntax in Paxter language.
On this page, we discuss these limitations.


## Escaping ‘@’

As readers have already noticed that ‘**@**’ symbol
has special meaning in Paxter language:
it acts as a switch which turns 
the subsequence piece of source text into a command.
Therefore, if Paxter library users wish to include ‘**@**’ string literal
as-is in the final HTML output, an escape of some sort is required.

… except that the core Paxter language specification actually
does _not_ provide a way to escape ‘**@**’ symbols per se.
However, there are a few ways around this.

### Method 1: Define Constants For ‘@’

We will take advantage of being able to run python code within the source text.
Specifically, we will define a variable to store the `@` symbol character.

```paxter
@python##"
at = '@'
"##
This is the @bold{at} symbol: @at.
```

```html
<p>This is the <b>at</b> symbol: @.</p>
```

But this method would not work when you wish to
write an email address or a twitter handle.
For this, additional bar-delimiters surrounding the phrase is needed
([see the next section of this page for more information](#escaping-delimiters-curly-braces-quotes-and-bars)).

```paxter
@python##"
at = '@'
"##
Email me at @link["mailto:person@example.com"]{person@|at|example.com}
and my twitter handle is @|at|example. Don’t @at me.
```

```html
<p>Email me at <a href="mailto:person@example.com">person@example.com</a>
   and my twitter handle is @example. Don’t @ me.</p>
```

### Method 2: Using `@verb` Command

The pre-defined `@verb` command (short for **verbatim**)
accepts a string argument and returns it as-is.
Here is an example of how to author the same document from the previous example.

```paxter
Email me at @link["mailto:person@example.com"]{@verb##"person@example.com"##}
and my twitter handle is @verb"@"example. @verb"Don’t @ me".
```

```html
<p>Email me at <a href="mailto:person@example.com">person@example.com</a>
   and my twitter handle is @example. Don’t @ me.</p>
```

### Method 3: Using Symbol-Only Command

Recall the {ref}`predefined-raw-html` section from a past page.
We have the commands `@\`, `@%`, `@.`, and `@,`
as shortcuts for some raw HTML strings.
In fact, commands under the symbol-only form 
may represent other kinds of objects as well.
Particularly in {mod}`paxter.author` subpackage,
we can display the string ‘**@**’ through the command `@@`.

Suppose we wish to include an email address in a blog post.
Here is an example of the source text:

```paxter
Email me at @link["mailto:person@example.com"]{person@@example.com}
and my twitter handle is @@example. Don’t @@ me.
```

The above source text gets transformed into the following HTML output.

```html
<p>Email me at <a href="mailto:person@example.com">person@example.com</a>
   and my twitter handle is @example. Don’t @ me.</p>
```

What would happen if we forgot to _double_ the `@` symbol?
Consider the following example source text.

```paxter
Email me at @link["mailto:person@example.com"]{person@@example.com}
and my twitter handle is @example. Don’t @@ me.
```

Parsing the above source text would yield the following error.
Essentially, the `@example` command at line 2 column 27 is an unknown command.
(The stack trace may be long and scary. It is totally to skim over it.)

```pytb
Traceback (most recent call last):
  File ".../paxter/src/paxter/evaluate/context.py", line 149, in transform_command
    phrase_value = phrase_eval(token.phrase, self.env)
  File ".../paxter/src/paxter/author/standards.py", line 31, in phrase_unsafe_eval
    return eval(phrase, env)
  File "<string>", line 1, in <module>
NameError: name 'example' is not defined

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File ".../paxter/venv/bin/paxter", line 33, in <module>
    sys.exit(load_entry_point('paxter', 'console_scripts', 'paxter')())
  File ".../paxter/venv/lib/python3.8/site-packages/click/core.py", line 829, in __call__
    return self.main(*args, **kwargs)
  File ".../paxter/venv/lib/python3.8/site-packages/click/core.py", line 782, in main
    rv = self.invoke(ctx)
  File ".../paxter/venv/lib/python3.8/site-packages/click/core.py", line 1259, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
  File ".../paxter/venv/lib/python3.8/site-packages/click/core.py", line 1066, in invoke
    return ctx.invoke(self.callback, **ctx.params)
  File ".../paxter/venv/lib/python3.8/site-packages/click/core.py", line 610, in invoke
    return callback(*args, **kwargs)
  File ".../paxter/src/paxter/__main__.py", line 99, in run_html
    document = run_document_paxter(input_text, env)
  File ".../paxter/src/paxter/author/preset.py", line 34, in run_document_paxter
    evaluate_context = EvaluateContext(input_text, env, parse_context.tree)
  File "<string>", line 6, in __init__
  File ".../paxter/src/paxter/evaluate/context.py", line 40, in __post_init__
    self.rendered = self.render()
  File ".../paxter/src/paxter/evaluate/context.py", line 43, in render
    return self.transform_fragment_list(self.tree)
  File ".../paxter/src/paxter/evaluate/context.py", line 120, in transform_fragment_list
    result = [
  File ".../paxter/src/paxter/evaluate/context.py", line 120, in <listcomp>
    result = [
  File ".../paxter/src/paxter/evaluate/context.py", line 117, in <genexpr>
    self.transform_fragment(fragment)
  File ".../paxter/src/paxter/evaluate/context.py", line 73, in transform_fragment
    return self.transform_command(fragment)
  File ".../paxter/src/paxter/evaluate/context.py", line 153, in transform_command
    raise PaxterRenderError(
paxter.exceptions.PaxterRenderError: paxter command phrase evaluation error at line 2 col 27: 'example'
```

(escaping-delimiters-curly-braces-quotes-and-bars)=
## Escaping Delimiters: Curly Braces, Quotes, and Bars

:::{admonition,caution} Under Construction
This section is under construction.
:::