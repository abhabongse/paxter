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
the specific syntax in the upcoming sections.

:::{admonition,info} Rule of Thumb
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

:::{admonition,info} Reminder
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

:::{admonition,info} Reminder
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
the phrase section followed by the main argument section.
Now it is time to introduce other variations of a command syntax,
especially those which contain the options section.

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
Notice that this command does not have the main argument section.
The options section of this commands accepts two arguments:
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

:::{note}
If you are thinking that the options section of a command syntax
looks eerily similar to function call syntax in python,
do take note that this happens by design.
We will dive into more details about the structure of command syntax
on later pages of this grand tutorial.
:::

:::{admonition,caution} TODO
Continue here.
:::

## Lists

## Tables

## Raw HTML

## Escapes

:::{admonition,caution} Under Construction
- Escaping `@` symbols
- Escaping `|...|`, `{...}`, and `"..."`
- Understanding python phrase evaluation and python function call translation
- Adding source code highlighting, etc.
:::
