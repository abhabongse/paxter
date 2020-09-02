# Evaluation Cycle Explained

On this page, we are going to see what happens under the hood
when a source text in Paxter language got parsed and interpreted.
Let us consider evaluating the following source text as our motivating example:

```paxter
Please visit @link["https://example.com"]{@italic{this} website}.
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

source_text = 'Please visit @link["https://example.com"]{@italic{this} website}.'
parsed_tree = ParserContext(source_text).tree
```

We can also see the content of the `parsed_tree` if we print them out.
However, feel free to skip over this big chunk of output
as they are not relevant to what we are discussing right now.

```pycon
>>> print(parsed_tree)
FragmentSeq(
    start_pos=0,
    end_pos=65,
    children=[
        Text(
            start_pos=0,
            end_pos=13,
            inner="Please visit ",
            enclosing=EnclosingPattern(left="", right=""),
        ),
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
                    Text(
                        start_pos=55,
                        end_pos=63,
                        inner=" website",
                        enclosing=EnclosingPattern(left="", right=""),
                    ),
                ],
                enclosing=EnclosingPattern(left="{", right="}"),
            ),
        ),
        Text(
            start_pos=64,
            end_pos=65,
            inner=".",
            enclosing=EnclosingPattern(left="", right=""),
        ),
    ],
    enclosing=GlobalEnclosingPattern(),
)
```

:::{admonition,tip} Dear Advanced Users
For those who are familiar with the study of Programming Languages,
this maybe enough to get you run wild!
Data definitions for parsed tree nodes
{ref}`can be seen here <parsing-data-definitions>`. 
:::   


## Step 2: Evaluating Parsed Tree Into Document Object
   
The `parsed_tree` from the previous step is evaluated
by a tree transformer from the {mod}`paxter.interpret` subpackage.
In general, what a parsed tree would be evaluated into
depends on each individual (meaning you, dear reader).

Paxter library decides to implement _one possible version_ of a tree transformer
called {class}`EvaluateContext <paxter.interpret.EvaluateContext>`.
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
created by the above function by default.

```python
from paxter.author.environ import create_document_env

env = create_document_env()
```

```pycon
>>> env
{'_phrase_eval_': <function paxter.author.standards.phrase_unsafe_eval(phrase: str, env: dict) -> Any>,
 '_extras_': {},
 '@': '@',
 'for': DirectApply(wrapped=<function for_statement at 0x7f80e279a280>),
 'if': DirectApply(wrapped=<function if_statement at 0x7f80e279a550>),
 'python': DirectApply(wrapped=<function python_unsafe_exec at 0x7f80f88fd790>),
 'verb': <function paxter.author.standards.verbatim(text: Any) -> str>,
 'raw': paxter.author.elements.RawElement,
 'paragraph': <bound method SimpleElement.from_fragments of <class 'paxter.author.elements.Paragraph'>>,
 'h1': <bound method SimpleElement.from_fragments of <class 'paxter.author.elements.Heading1'>>,
 'h2': <bound method SimpleElement.from_fragments of <class 'paxter.author.elements.Heading2'>>,
 'h3': <bound method SimpleElement.from_fragments of <class 'paxter.author.elements.Heading3'>>,
 'h4': <bound method SimpleElement.from_fragments of <class 'paxter.author.elements.Heading4'>>,
 'h5': <bound method SimpleElement.from_fragments of <class 'paxter.author.elements.Heading5'>>,
 'h6': <bound method SimpleElement.from_fragments of <class 'paxter.author.elements.Heading6'>>,
 'bold': <bound method SimpleElement.from_fragments of <class 'paxter.author.elements.Bold'>>,
 'italic': <bound method SimpleElement.from_fragments of <class 'paxter.author.elements.Italic'>>,
 'uline': <bound method SimpleElement.from_fragments of <class 'paxter.author.elements.Underline'>>,
 'code': <bound method SimpleElement.from_fragments of <class 'paxter.author.elements.Code'>>,
 'blockquote': <bound method Blockquote.from_fragments of <class 'paxter.author.elements.Blockquote'>>,
 'link': <bound method Link.from_fragments of <class 'paxter.author.elements.Link'>>,
 'image': paxter.author.elements.Image,
 'numbered_list': <bound method EnumeratingElement.from_direct_args of <class 'paxter.author.elements.NumberedList'>>,
 'bulleted_list': <bound method EnumeratingElement.from_direct_args of <class 'paxter.author.elements.BulletedList'>>,
 'table': <bound method SimpleElement.from_direct_args of <class 'paxter.author.elements.Table'>>,
 'table_header': <bound method EnumeratingElement.from_direct_args of <class 'paxter.author.elements.TableHeader'>>,
 'table_row': <bound method EnumeratingElement.from_direct_args of <class 'paxter.author.elements.TableRow'>>,
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

:::{admonition,caution} Under Construction
Continue here.
:::

## Step 3: Rendering Document Object

Recall the [basic principles](command-a-basic-building-block)
mentioned on the previous page:
every command, regardless of the assumed syntactical form,
_always_ consists of the following components.

1. The onset `"@"` symbol
2. The phrase part (such as )

