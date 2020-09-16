# Evaluation Cycle Explained

On this page, we are going to see what happens under the hood
when a source text in Paxter language got parsed and interpreted.
Let us consider evaluating the following source text as our motivating example:

```paxter
Please visit @link["https://example.com"]{@italic{this} website}. @line_break
@image["https://example.com/hello.jpg", "hello"]
```

We are going to assume that we use the function
{func}`run_document_paxter <paxter.author.preset.run_document_paxter>`
in order to evaluate the above source text into the final HTML output.
This transformation can be divided into three logical steps.

1. Parsing source text
2. Evaluating parsed tree into document object
3. Rendering document object


## Step 1: Parsing Source Text

Specifically, the core {mod}`paxter.parse` subpackage
implements a parser, {class}`ParseContext <paxter.parse.ParseContext>`,
which parses a source text (written in Paxter language) into the parsed tree form.
Here is how to use python API to run this step.
   
```python
from paxter.parse import ParserContext

source_text = '''Please visit @link["https://example.com"]{@italic{this} website}. @line_break
@image["https://example.com/hello.jpg", "hello"]'''
parsed_tree = ParserContext(source_text).tree
```

We can also see the content of the `parsed_tree` if we print them out.
However, feel free to skip over this big chunk of output
as they are not relevant to what we are discussing right now.

```pycon
>>> print(parsed_tree)
FragmentSeq(
    start_pos=0,
    end_pos=126,
    children=[
        Text(start_pos=0, end_pos=13, inner="Please visit ", enclosing=EnclosingPattern(left="", right="")),
        Command(
            start_pos=14,
            end_pos=64,
            phrase="link",
            phrase_enclosing=EnclosingPattern(left="", right=""),
            options=TokenSeq(
                start_pos=19,
                end_pos=40,
                children=[
                    Text(
                        start_pos=20,
                        end_pos=39,
                        inner="https://example.com",
                        enclosing=EnclosingPattern(left='"', right='"'),
                    )
                ],
            ),
            main_arg=FragmentSeq(
                start_pos=42,
                end_pos=63,
                children=[
                    Command(
                        start_pos=43,
                        end_pos=55,
                        phrase="italic",
                        phrase_enclosing=EnclosingPattern(left="", right=""),
                        options=None,
                        main_arg=FragmentSeq(
                            start_pos=50,
                            end_pos=54,
                            children=[
                                Text(
                                    start_pos=50,
                                    end_pos=54,
                                    inner="this",
                                    enclosing=EnclosingPattern(left="", right=""),
                                )
                            ],
                            enclosing=EnclosingPattern(left="{", right="}"),
                        ),
                    ),
                    Text(start_pos=55, end_pos=63, inner=" website", enclosing=EnclosingPattern(left="", right="")),
                ],
                enclosing=EnclosingPattern(left="{", right="}"),
            ),
        ),
        Text(start_pos=64, end_pos=66, inner=". ", enclosing=EnclosingPattern(left="", right="")),
        Command(
            start_pos=67,
            end_pos=77,
            phrase="line_break",
            phrase_enclosing=EnclosingPattern(left="", right=""),
            options=None,
            main_arg=None,
        ),
        Text(start_pos=77, end_pos=78, inner="\n", enclosing=EnclosingPattern(left="", right="")),
        Command(
            start_pos=79,
            end_pos=126,
            phrase="image",
            phrase_enclosing=EnclosingPattern(left="", right=""),
            options=TokenSeq(
                start_pos=85,
                end_pos=125,
                children=[
                    Text(
                        start_pos=86,
                        end_pos=115,
                        inner="https://example.com/hello.jpg",
                        enclosing=EnclosingPattern(left='"', right='"'),
                    ),
                    Operator(start_pos=116, end_pos=117, symbols=","),
                    Text(start_pos=119, end_pos=124, inner="hello", enclosing=EnclosingPattern(left='"', right='"')),
                ],
            ),
            main_arg=None,
        ),
    ],
    enclosing=GlobalEnclosingPattern(),
)
```

:::{admonition,tip} Dear Advanced Users
For those who are familiar with the field of Programming Languages,
this maybe enough to get you run wild!
See the [syntax reference](../references/syntax.md)
and the {ref}`data definitions for parsed tree nodes <parsing-data-definitions>`
to help get started right away.
:::   


## Step 2: Evaluating Parsed Tree Into Document Object
   
The `parsed_tree` from the previous step is then interpreted
by a tree transformer from the {mod}`paxter.interpret` subpackage.
In general, what a parsed tree would be evaluated into
depends on each individual (meaning you, dear reader).

Paxter library decides to implement _one possible version_ of a tree transformer
called {class}`InterpreterContext <paxter.interpret.context.InterpreterContext>`.
This particular transformer tries to 
**mimic the behavior of calling python functions** as closest possible.
In addition, this transformer expects what is called 
the **initial environment dictionary**  under which python executions are performed.
For this particular scenario, this dictionary is created by the function
{func}`create_document_env <paxter.author.environ.create_document_env>`
from the {mod}`paxter.author` subpackage.
This environment dictionary contains the mapping of
function aliases to the actual python functions and object
and it is where the magic happens.

Let us look at the contents of the environment dictionary
created by the above function
{func}`create_document_env <paxter.author.environ.create_document_env>`.

```python
from paxter.author.environ import create_document_env

env = create_document_env()
```

```pycon
>>> env
{'_phrase_eval_': <function paxter.author.standards.phrase_unsafe_eval>,
 '_extras_': {},
 '@': '@',
 'for': <function paxter.author.controls.for_statement>,
 'if': <function paxter.author.controls.if_statement>,
 'python': <function paxter.author.standards.python_unsafe_exec>,
 'verb': <function paxter.author.standards.verbatim>,
 'raw': <class paxter.author.elements.RawElement>,
 'paragraph': <classmethod paxter.author.elements.SimpleElement.from_fragments>,
 'h1': <classmethod paxter.author.elements.SimpleElement.from_fragments>,
 'h2': <classmethod paxter.author.elements.SimpleElement.from_fragments>,
 'h3': <classmethod paxter.author.elements.SimpleElement.from_fragments>,
 'h4': <classmethod paxter.author.elements.SimpleElement.from_fragments>,
 'h5': <classmethod paxter.author.elements.SimpleElement.from_fragments>,
 'h6': <classmethod paxter.author.elements.SimpleElement.from_fragments>,
 'bold': <classmethod paxter.author.elements.SimpleElement.from_fragments>,
 'italic': <classmethod paxter.author.elements.SimpleElement.from_fragments>,
 'uline': <classmethod paxter.author.elements.SimpleElement.from_fragments>,
 'code': <classmethod paxter.author.elements.SimpleElement.from_fragments>,
 'blockquote': <classmethod paxter.author.elements.Blockquote.from_fragments>,
 'link': <classmethod paxter.author.elements.Link.from_fragments>,
 'image': <class paxter.author.elements.Image>,
 'numbered_list': <classmethod paxter.author.elements.EnumeratingElement.from_direct_args>,
 'bulleted_list': <classmethod paxter.author.elements.EnumeratingElement.from_direct_args>,
 'table': <classmethod paxter.author.elements.SimpleElement.from_direct_args>,
 'table_header': <classmethod paxter.author.elements.EnumeratingElement.from_direct_args>,
 'table_row': <classmethod paxter.author.elements.EnumeratingElement.from_direct_args>,
 'hrule': RawElement(body='<hr />'),
 'line_break': RawElement(body='<br />'),
 '\\': RawElement(body='<br />'),
 'nbsp': RawElement(body='&nbsp;'),
 '%': RawElement(body='&nbsp;'),
 'hairsp': RawElement(body='&hairsp;'),
 '.': RawElement(body='&hairsp;'),
 'thinsp': RawElement(body='&thinsp;'),
 ',': RawElement(body='&thinsp;')}
```

It is crucial to point out that,
all of the commands we have seen so far
on the page [](quick-blogging.md)
(e.g. `bold`, `h1`, `blockquote`, `numbered_list`, `table`, and many others)
are some keys of the `env` dictionary object as listed above.
This is _not_ a coincidence.
Essentially, Paxter library utilizes the data from this dictionary
in order to properly interpret each command in the source text.

(interpreting-a-command)=
### Interpreting a Command

The process of interpreting a command is divided into two steps:
resolving the phrase and invoking a function call.
Let us explore each step assuming the initial environment dictionary `env`
(borrowed from above). 

1.  **Resolve the phrase part.**
    By default, the phrase part is used as the key for looking up
    a python value from the environment dictionary `env`.
    For example, resolving the phrase `italic` from the command `@italic{...}`
    would yield the value of `env["italic"]`
    which refers to 
    {meth}`Italic.from_fragments <paxter.author.elements.SimpleElement.from_fragments>`
    class method.
    Likewise, the phrase `link` from the command `@link["target"]{text}` maps to 
    {meth}`Link.from_fragments <paxter.author.elements.Link.from_fragments>`
    under the dictionary `env`.
    
    :::{admonition,important} Backup Plan
    However, if the key which is made of the phrase part
    does not appear in `env` dictionary,
    then the backup plan is to use python built-in function {func}`eval`
    to **evaluate the entire phrase string** with `env` as the global namespace.
    This fallback behavior enables a myriad of features in Paxter ecosystem
    including evaluating an anonymous python expression
    from right within the source text.
    In order to encode any string as the phrase of a command,
    we need to introduce a slightly different syntactical form of a command,
    which we would cover {ref}`in a later tutorial <evaluating-python-expressions>`,
    but here is a little taste of that:
    
    ```paxter
    The result of 7 * 11 * 13 is @|7 * 11 * 13|.
    ```
    
    ```html
    <p>The result of 7 * 11 * 13 is 1001.</p>
    ```
    :::
    
    :::{admonition,caution} Noteworthy
    The resolution of the phrase part of a command into a python value
    can be fully customized by replacing `env["_phrase_eval_"]`
    with another function of the identical signature.
    This default behavior described above is merely of the default function
    located at `env["_phrase_eval_"]`.
    :::

2.  **Invoke a function call.**
    Before we continue, if the original command contains
    _neither_ the options _nor_ the main argument parts,
    then the python object returned from step 1
    will not be further process
    and will immediately become the final output 
    of the command interpretation.

    Otherwise, the available options part and the main argument part
    will all become input arguments of a function call
    to the object returned by the previous step.
    Of course, that python object is expected to be callable in order to work.
    Particularly,
    
    - If the main argument part exists,
      its value will always be the very first input argument of the function call.
      If the options part also exists,
      then each of its items (separated by commas)
      will be subsequent arguments of the function call.
    - If the main argument part does not exist,
      then all of the items from the options part
      will be sole input arguments of the function call.
      
Let us walkthrough these two-step process with a few examples.

#### Example 1: Non-Callable Command

Let us begin with a basic example.
The command `@line_break` on its own would get translated roughly
into the following python code equivalent.
The final result is stored inside the variable `result`.

```python
# Step 1: resolving the phrase
line_break_obj = env['line_break']  # paxter.author.elements.line_break
# Step 2 is skipped since there is no function call
result = line_break_obj
```

#### Example 2: Command With Main Argument

Consider the command `@italic{this}`.
It would be transformed into the following python equivalent:

```python
# Step 1: resolving the phrase
italic_obj = env['italic']  # paxter.author.elements.Italic.from_fragments
# Step 2: function call
result = italic_obj(FragmentList(["this"]))
```

Notice that the main argument part `{this}` of the command `@italic{this}`
gets translated to `FragmentList(["this"])` in python representation.
In Paxter’s terminology, any component of the command syntax
which is enclosed by a pair of matching curly braces
would be known as **a fragment list**,
and it would be represented as a list of subtype
{class}`FragmentList <paxter.interpret.data.FragmentList>`.

#### Example 3: Command With Both Options and Main Argument

Let us look at this rather complicated command
and its python code equivalent.

```paxter
@link["https://example.com"]{@italic{this} website}
```

```python
# Step 1: resolving the phrases
italic_obj = env['italic']  # paxter.author.elements.Italic.from_fragments
link_obj = env['link']  # paxter.author.elements.Link.from_fragments

# Step 2: function call
result = link_obj(
    FragmentList([
        italic_obj(FragmentList(["this"])),  # just like previous example
        " website",
    ]),
    "https://example.com",
)
```

There are a few notes to point out:
- The first input argument of the function call to `link_obj`
  derives from the main argument fragment list,
  which contains the nested function call to `italic_obj`.
- The target URL `"https://example.com"` appeared in the options part of the `@link` command
  becomes the second argument in the function call to `link_obj`.
  
To provide further clarification of how a command in Paxter source text gets translated,
consider the following example where a command 
contains two argument items within its options part.

```paxter
@foo["bar", 3]{text}
```

```python
# Step 1: resolving the phrases
foo_obj = env['foo']
# Step 2: function call
result = foo_obj(FragmentList(["text"]), "bar", 3)
```

Python-style keyword arguments are also supported within the options part,
and it works in the way we expect.

```paxter
@foo["bar", n=3]{text}
```

```python
# Step 1: resolving the phrase
foo_obj = env['foo']
# Step 2: function call
result = foo_obj(FragmentList(["text"]), "bar", n=3)
```

#### Example 4: Commands With Options Only

In the master example at the beginning of this page,
we can see the following `@image` command:

```paxter
@image["https://example.com/hello.jpg", "hello"]
```

Because the main argument part is not present inside the `@image` command,
the above source text would be interpreted similarly to the following python code.

```python
# Step 1: resolving the phrase
image_obj = env['image']  # paxter.author.elements.Image
# Step 2: function call
result = image_obj("https://example.com/hello.jpg", "hello")
```

Is there a way to make a function call to the object with zero arguments?
Of course. It can be done by writing square brackets containing nothing inside it.

```paxter
@foo[]
```

```python
# Step 1: resolving the phrase
foo_obj = env['foo']
# Step 2: function call
result = foo_obj()
```

Beware _not_ to use curly braces in place of square brackets
as it would have resulted in slightly different interpretation,
like in the following.

```paxter
@foo{}
```

```python
# Step 1: resolving the phrase
foo_obj = env['foo']
# Step 2: function call
result = foo_obj(FragmentList([]))
```

### Motivating Example Revisited

By combining all of the above examples,
we can describe the semantics of the motivating example
as shown in the following python code 
(the original source text is reproduced below for convenience):

```paxter
Please visit @link["https://example.com"]{@italic{this} website}. @line_break
@image["https://example.com/hello.jpg", "hello"]
```

```python
# Step 1: resolving the phrases
italic_obj = env['italic']  # paxter.author.elements.Italic.from_fragments
link_obj = env['link']  # paxter.author.elements.Link.from_fragments
line_break_obj = env['line_break']  # paxter.author.elements.line_break
image_obj = env['image']  # paxter.author.elements.Image

# Step 2: function call
document_result = FragmentList([
    "Please visit ",
    link_obj(
        FragmentList([
            italic_obj(FragmentList(["this"])),
            " website",
        ]),
        "https://example.com",
    ),
    ". ",
    line_break_obj,
    "\n",
    image_obj("https://example.com/hello.jpg", "hello"),
])
```

However, the actual python API to replicate the above result is as follows
(where `parsed_tree` is the result borrowed from step 1).

```python
from paxter.author.environ import create_document_env
from paxter.interpret.context import InterpreterContext

env = create_document_env()
document_result = InterpreterContext(source_text, env, parsed_tree).rendered
```

The result of interpreting the entire source text
using {class}`InterpreterContext <paxter.interpret.context.InterpreterContext>`
is always going to be a fragment list of each smaller pieces of content
(which is why the `document_result` in the above code is an instance of
{class}`FragmentList <paxter.interpret.data.FragmentList>` class).
Displaying the content of `document_result` gives us the following evaluated result.

```pycon
>>> document_result
FragmentList([
    "Please visit ",
    Link(body=[Italic(body=["this"]), " website"], href="https://example.com"),
    ". ",
    RawElement(body="<br />"),
    "\n",
    Image(src="https://example.com/hello.jpg", alt="hello"),
])
```


## Step 3: Rendering Document Object

:::{admonition,important} Reminder Again
In all truthfulness, rendering the `final_result` into HTML string output
has _nothing_ to do with the core Paxter language specification.
In fact, if library users implement their own version of parsed tree evaluator,
this particular step would be non-existent.
:::

Rendering the entire `document_result` into HTML string output is simple.
Two small steps are required:

1. Wrap the `document_result` with {class}`Document <paxter.author.elements.Document>`
2. Invoke the {meth}`html <paxter.author.elements.Element.html>` method.

And here is the python code to do exactly as just said:

```python
from paxter.author.elements import Document

document = Document.from_fragments(document_result)
html_output = document.html()
```

This yields the following final HTML output:

```pycon
>>> print(html_output)
<p>Please visit <a href="https://example.com"><i>this</i> website</a>. <br />
<img src="https://example.com/hello.jpg" alt="hello" /></p>
```

:::{admonition,info} Preset Function
The preset function {func}`run_document_paxter <paxter.author.preset.run_document_paxter>`
introduced in the section {ref}`Programmatic Usage <method-2-programmatic-usage>`
(from Getting Started page) simply performs all three steps as mentioned above in order.
:::
