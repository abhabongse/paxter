# Quick Blogging

To quickly get started with blogging or writing an article,
we introduce the Paxter language syntax
as being _preconfigured_ by {mod}`paxter.author` subpackage
which can be used to write rich-formatted content.

:::{admonition,caution} Beware 
Most of the descriptions about the syntax shown on this page
are specific to the preconfigured variation of Paxter language
provided by {mod}`paxter.author` subpackage.
It is actually _not_ tied to the core Paxter language specification.

Paxter library (which includes the core Paxter language specification)
is designed to be very extensible and customizable.
The {mod}`paxter.author` subpackage is merely
supplementary provided by Paxter library for convenience.
It is entirely possible to utilize Paxter library _without_ touching
any of the {mod}`paxter.author` whatsoever,
as being demonstrated in the
{doc}`intermediate tutorials <../intermediate-tutorials/index>` section.
:::


(command-a-basic-building-block)=
## Command: A Basic Building Block

**A command** is the core building block in Paxter language.
It has various syntactical forms, but all of them have the same basic principles:

- Each command always begin with an `@` symbol in the source text.
- Each command always has the **phrase part**
  which immediately follows the initial `@` symbol.
- Each command may optionally have what is called the **options part**.
  If it exists, it has the form of `[...]` that follows the phrase part.
- Each command may optionally have what is called the **main argument part**.
  If it exists, it follows the phrase part
  or the options part (if the options part exists).

This may sound confusing right now.
Hopefully things will get clearer as we discuss
the specific syntax on the page [](evaluation-cycle-explained.md).

:::{admonition,important} Rule of Thumb
A rule of thumb to remember about the core Paxter language
is that it dictates only how a command in the source text should be parsed.
It has no bearing on how each parsed command and any other raw text
are to be interpreted or evaluated into the desired final output.
For descriptions of syntax appeared on this page,
this interpretation is done by the supplementary {mod}`paxter.author` subpackage.
:::


## Bolds, Italics, and Underline

Let us begin with “bolding” part of a source text.
We use the command `@bold{...}`,
replacing `...` with the actual text to be emphasized.
In this particular command, `bold` is the phrase part
whereas the emphasized text is the main argument part of the command.

For example, consider the following source text written in Paxter language.

```paxter
This is a very @bold{important part} of the statement.
```

This source text will be transformed to the following HTML output.

```html
<p>This is a very <b>important part</b> of the statement.</p>
```

And likewise, for italicized text and underlined text,
use the command `@italic{...}` and `@uline{...}` respectively.
Notice that we altered the phrase part of the command
while the the main argument parts remains the same.

```paxter
This is a very @italic{important part} of @uline{the statement}.
```

This source text will be transformed to the following HTML output.

```html
<p>This is a very <i>important part</i> of <u>the statement</u>.</p>
```


### Aside: Nested commands

One nice thing about Paxter command is that they are allowed
to be nested inside the main argument between the pair of curly braces.
For example,

```paxter
This is @italic{so important that @uline{multiple emphasis} is required}.
```

When the above source text get rendered into HTML,
we obtain the following result.

```html
<p>This is <i>so important that <u>multiple emphasis</u> is required</i>.</p>
```


## Monospaced Code

Similarly to what we have seen with
`@bold{...}`, `@italic{...}`, and `@uline{...}` from above,
we use the command `@code{...}` to encapsulate text
to be displayed as monospaced code.

For example, the following source text written in Paxter language

```paxter
Run the @code{python} command.
```

will be evaluated into the HTML output shown below.

```html
<p>Run the <code>python</code> command.</p>
```


## Multiple Paragraphs

To write multiple paragraphs,
simply separate chunks of texts with at least two newline characters
(i.e. there must be a blank line between consecutive paragraphs).
Each chunk of text will result in its own paragraph.
Consider the following example containing exactly three paragraphs.

```paxter
This is @bold{the first paragraph}.
This is the second sentence of the first paragraph.

This is @italic{another} paragraph.

This is the @uline{final} paragraph.
```

The above text in Paxter language will be transformed
into the following HTML.

```html
<p>This is <b>the first paragraph</b>.
   This is the second sentence of the first paragraph.</p>
<p>This is <i>another</i> paragraph.</p>
<p>This is the <u>final</u> paragraph.</p>
```

:::{admonition,tip} Reminder
The implicit paragraph splitting behavior of the source text
is preconfigured by the supplementary {mod}`paxter.author` subpackage
and has nothing to do with the core Paxter language specification.
:::


## Headings

To include a heading (from level 1 down to level 6)
use the command `@h1{...}` through `@h6{...}` on its own chunk.
They must be separated from other paragraph chunks
with at least one blank line.

```paxter
@h1{New Blog!}

@bold{Welcome to the new blog!} Let’s celebrate!

@h2{Updates}

There is no update.
```

```html
<h1>New Blog!</h1>
<p><b>Welcome to the new blog!</b> Let’s celebrate!</p>
<h2>Updates</h2>
<p>There is no update.</p>
```

Observe that if the `@h1{...}` and `@h2{...}`
were removed from encapsulating the heading text,
they would have been rendered as its own paragraph.
Try that to see for yourself.

Also, what happens if the command `@h1{...}`
accidentally did _not_ surround the entire chunk of text?
Let us look at this example in which
the exclamation mark is located _outside_ of the command:

```paxter
@h1{New Blog}!

@bold{Welcome to the new blog!} Let’s celebrate!
```

```html
<p><h1>New Blog</h1>!</p>
<p><b>Welcome to the new blog!</b> Let’s celebrate!</p>
```

Since *not* the entire chunk of heading text
is encapsulated by the `@h1{...}` command,
Paxter assumes that it is simply just a paragraph.
So beware of this kind of errors.


## Blockquote

The `@blockquote{...}` command must reside on its own chunk
just like a heading command.
So the following Paxter source text

```paxter
They said that

@blockquote{I refuse.}
```

would be transformed into the following HTML output.

```html
<p>They said that</p>
<blockquote>I refuse.</blockquote>
```

However, suppose that we want to include multiple paragraphs inside the blockquote.
We can follow the similar rules
as to how to write multiple paragraphs in general:
by separating them with at least one blank lines.
This is demonstrated in the following example.

```paxter
They said that

@blockquote{
    I refuse.

    Then I regret.
}
```

```html
<p>They said that</p>
<blockquote>
    <p>I refuse.</p>
    <p>Then I regret.</p>
</blockquote>
```

The important key to note here is that,
each paragraph within the blockquote will be surrounded by
a paragraph tag `<p>...</p>`
as long as more than one chunk of text exists.

:::{admonition,tip} Reminder
This particular behavioral rule is enforced by
{mod}`paxter.author` mainly for convenience.
Again, it has nothing to do with the core Paxter language specification.
:::


### Aside: Manual Paragraph Annotation

However, if we wish to force wrap the only paragraph within the blockquote
with a paragraph tag,
we can manually wrap that part of text with the `@paragraph{...}` command.
Let us reconsider the first example of this section again.
If we wish to have a paragraph tag surround the text “I refuse.”,
then we can write as follows.

```paxter
They said that

@blockquote{@paragraph{I refuse.}}
```

And we would get the following HTML output.

```html
<p>They said that</p>
<blockquote><p>I refuse.</p></blockquote>
```

By the way, do you remember when an entire chunk of text
was contained within a command such as `@h1{...}`?
As a result, that particular chunk of text
did not get treated with paragraph tag `<p>...</p>`.
While this behavior is desirable for heading commands,
it is not the case for other inline commands such as `@bold{...}`,
`@italics{...}` or `@uline{...}`.
For these commands, explicit `@paragraph{...}` is needed.

```paxter
@bold{Bold text without paragraph encapsulation.}

@paragraph{@bold{Bold text paragraph.}}
```

```html
<b>Bold text without paragraph encapsulation.</b>
<p><b>Bold text paragraph.</b></p>
```


## Links and Images

So far, all of the commands we have seen on this page contains
the phrase section followed by the main argument part.
Now it is time to introduce other variations of a command syntax,
especially those which contain the options part.

To put a link such as a URL on a piece of text,
we use the command `@link["target"]{text}`
replacing the `"target"` with the string literal
containing the actual target URL.
The displaying text would still be those in between the curly braces.

Here is an example of the usage of the `@link` command.

```paxter
Click @link["http://example.com"]{here} to go to my website.
```

```html
<p>Click <a href="http://example.com">here</a> to go to my website.</p>
```

Next, to insert an image, we use the command `@image["srcpath", "alt"]`.
Notice that this command does not have the main argument part.
The options part of this commands accepts two arguments:
the first one being the string literal containing the URL path to the image
and the second one is for the image alternative text.
In fact, the second argument is actually *not* required
and will default to an empty string.
For example,

```paxter
@image["http://example.com/hello.png", "hello"]

@image["http://example.com/bye.png"]
```

The above Paxter text will be rendered into the following HTML.

```html
<img src="http://example.com/hello.png" alt="hello" />
<img src="http://example.com/bye.png" alt="" />
```

:::{admonition,note} Notice
If you are thinking that the options part of a command syntax
looks eerily similar to function call syntax in python,
do take note that this happens by design.
We will dive into more details about the structure of command syntax
on the page [](evaluation-cycle-explained.md).
:::


## Lists

There are two kinds of list enumerations: numbered list and bulleted list
(sometimes known as ordered and unordered lists respectively).
To create a numbered list, use the `@numbered_list[...]` command
where each argument of the options part represents an item of the list.
The textual content for each item must be enclosed by a pair of curly braces
like in the following example.

```paxter
@numbered_list[
    {This is the first item.},
    {This is the @italic{second} item.},
    {This is the last item.},
]
```

```html
<ol>
    <li>This is the first item.</li>
    <li>This is the <i>second</i> item.</li>
    <li>This is the last item.</li>
</ol>
```

Similarly, for bulleted list, use `@bulleted_list[...]` command
with the similar structure.

What happens there are more than one chunk of text
separated by a single blank line within one of the items of the list?
The paragraph splitting rules for `@blockquote{...}` also applies here,
as demonstrated in the following example.

```paxter
@bulleted_list[
    {
        @bold{Rule number one.} Be clear.

        Very clear indeed.
    },
    {@bold{Rule number two.} Be consistent.},
]
```

```html
<ul>
    <li>
        <p><b>Rule number one.</b> Be clear.</p>
        <p>Very clear indeed.</p>
    </li>
    <li><b>Rule number two.</b> Be consistent.</li>
</ul>
```

And yes, if there is only one paragraph and the explicit tag is needed,
wrap the content with the `@paragraph{...}` command.


## Tables

Essentially, a table is a sequence of rows, and each row is a sequence of cells.
To construct a table, we use the command `@table[...]`
where each argument within the options part must be a command of the form
`@table_header[...]` for table header rows
or `@table_row[...]` for table data rows.
In turn, each cell within a table row would be wrapped in curly braces
and presented as an argument inside the options part of 
`@table_header[...]` or `@table_row[...]`

To demystify this tedious explanation, consider the following example.

```paxter
@table[
    @table_header[{No.}, {Name}, {Age}],
    @table_row[
        {1},
        {FirstnameA LastnameA},
        {21},
    ],
    @table_row[
        {2},
        {FirstnameB LastnameB},
        {34},
    ],
    @table_row[
        {3},
        {FirstnameC LastnameC},
        {55},
    ],
]
```

```html
<table>
    <tr>
        <th>No.</th>
        <th>Name</th>
        <th>Age</th>
    </tr>
    <tr>
        <td>1</td>
        <td>FirstnameA LastnameA</td>
        <td>21</td>
    </tr>
    <tr>
        <td>2</td>
        <td>FirstnameB LastnameB</td>
        <td>34</td>
    </tr>
    <tr>
        <td>3</td>
        <td>FirstnameC LastnameC</td>
        <td>55</td>
    </tr>
</table>
```

Paragraph splitting rules also applies to each cell data
just like within a blockquote or within an item of a list.


## Raw HTML

In HTML, symbols such as `&`, `<`, `>`, and `"` requires **escaping**
in order to be properly displayed in the rendered output
(in the form of `&amp;`, `&lt;`, `&gt;`, and `&quot;` respectively).
For HTML rendering performed by the {mod}`paxter.author` subpackage,
the escaping of these special characters are automatically done
for both convenience and safety reasons.

However, there might be times you wish to include HTML tags or
[HTML entities](https://html.spec.whatwg.org/multipage/named-characters.html#named-character-references)
such as `<del>...</del>` or `&ndash;`.
This can be done using the command of the form `@raw"text"`.
For example,

```paxter
Let’s count A&ndash;Z.

No, I mean A@raw"&ndash;"Z!

Use <del>...</del> for @raw"<del>"strikethrough@raw"</del>" text. 
```

```html
<p>Let’s count A&amp;ndash;Z.</p>
<p>No, I mean A&ndash;Z!</p>
<p>Use &lt;del&gt;...&lt;/del&gt; for <del>strikethrough</del> text.</p>
```

And this is how the above HTML code is displayed:

```{raw} html
<blockquote>
    <p>Let’s count A&amp;ndash;Z.</p>
    <p>No, I mean A&ndash;Z!</p>
    <p>Use &lt;del&gt;...&lt;/del&gt; for <del>strikethrough</del> text.</p>
</blockquote>
```

(predefined-raw-html)=
### Pre-defined Raw HTML

For convenience, the {mod}`paxter.author` has already defined
a few of common raw HTML strings for use, as shown below.

| Command | HTML equivalent | Meaning |
| ------- | --------------- | ------- |
| `@hrule` | `<hr />` | Thematic break |
| `@line_break`, `@\` | `<br />` | Line break |
| `@nbsp`, `@%` | `&nbsp;` | Non-breaking space |
| `@hairsp`, `@.` | `&hairsp;` | Hair space |
| `@thinsp`, `@,` | `&thinsp;` | Thin space |

:::{admonition,caution} Notes about commands in the above table
- Every command shown in the table expects
  _neither_ the options part _nor_ the main argument part.
  This is one valid form of a command in Paxter language.
- Observe that there is a rather unusual form of a command,
  which consists of the `"@"` symbol immediately followed by another symbol character
  (namely `@\`, `@%`, `@.`, and `@,`).
  This is called the **symbol-only form**.
  The parsing rules of this kind of command is distinct
  from other commands we have seen up until this point. 
  Specific differences will be discussed on later pages in this documentation.
:::

Here is some usage example.

```paxter
The store opens Monday@,-@,Friday @line_break 9@%AM@,-@,5@%PM.evaluate-and-execute-python-code

@hrule
```

```html
<p>The store opens Monday&thinsp;-&thinsp;Friday <br />
   9&nbsp;AM&thinsp;-&thinsp;5&nbsp;PM.</p>
<hr />
```
