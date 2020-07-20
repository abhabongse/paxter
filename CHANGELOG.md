# Changelog

## 0.6.5 (20 July 2020)

-   Remove encapsulated outermost `<div>` tag from the HTML rendered result
    of the Python document authoring mode.
-   Add `NormalApplyWithEnv` wrapper which will 
    additionally provides environment as the very first argument 
    before the all the positional and keyword arguments of the wrapped function.

## 0.6.4 (20 July 2020)

-   Moved the HTML escape from the visitor into the document element renderers.

## 0.6.3 (20 July 2020)

-   Fixed bug where function `create_unsafe_document_env` breaks
    when the input argument for outside environment is not supplied.
-   Make all document element classes dataclasses.

## 0.6.2 (17 July 2020)

-   In both Python string authoring mode and Python document authoring mode,
    by default `@!` and `@@` will be transformed into empty string and  `@`
    respectively.

## 0.6.1 (15 July 2020)

-   The function `paxter.pyauthor.create_unsafe_env` is renamed to
    `paxter.pyauthor.create_unsafe_bare_env`.
-   Introduce document python authoring mode
    using `paxter.pyauthor.create_unsafe_document_env`.

## 0.6.0 (6 July 2020)

-   No longer allows @-expresion text and fragment list within fragment list itself.
-   @-switch is no longer needed when embedding texts or fragment lists
    within the option section of a command.
-   Single symbol command (such as `@@` and `@,`) are now its own node type.
    
## 0.5.0 (14 June 2020)

-   Once again, the entire Paxter language grammar is re-designed.
    _No longer compatible with all previous versions._
-   The identifier section of function-call @-expressions (called a “command”)
    and the phrase expression in unified into the same pattern.
    Now, it is possible to evaluate a phrase expression into a function
    and use it in the function-call @-expression.

## 0.4.0 (7 May 2020)

-   The entire Paxter language grammar is re-designed from the ground up. 
    _No longer compatible with all previous versions._
-   Parsed tree transformers are now called renderers.
-   Simple Snake flavor of tree transformers (i.e. renderers) 
    are removed and no longer exists.
-   ReadTheDocs documentation is now set up.

## 0.3.0 (14 March 2020)

-   Changes in Paxter language Specification
    -   `PaxterMacro` now allows options just like `PaxterFunc`
    -   For each key-value pair in an option list,
        the key part now becomes optional in place of the value part.  
        Therefore, the option list of the form `[1,"2",v3,k4=4,k5="5",k6=v6]`
        is a valid Paxter language syntax
        (formerly, the first two key-value pairs were unacceptable).
-   New utility decorators in Simple Snake: 
    `with_env`, `with_node`, and `DefinitionSet`.
-   Way better unit test coverages and docstrings

## 0.2.0 (12 March 2020)

-   Optimized parser (remove redundant steps, refactor code, etc.)
-   Package reorganization (e.g. flavored tree transformers now in `paxter.flavors`)
-   **Simple Snake** behavior changes:
    -    A line ending with backslash will remove the backslash itself 
         along with the newline character next to it
    -    Introduce `@load!` macro to load pre-defined functions
    -    Introduce `@if` and `@for` special functions
-   Better unit test coverages and docstrings

## 0.1.3 (7 March 2020)

-   Remove debugging print statement from transformer

## 0.1.2 (7 March 2020)

-   Fixed missing quotation mark rule in JSON string literal lexer
-   Introduced simple python-flavored parsed tree transformer

## 0.1.1 (7 March 2020)

-   Added python 3.7 trove in PyPI display

## 0.1.0 (7 March 2020)

-   First release on PyPI.
