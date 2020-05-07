# Changelog

## 0.4.0 (7 May 2020)

-   The entire Paxter language grammar is re-designed from the ground up. _No longer compatible with all previous versions._
-   Parsed tree transformers are now called renderers.
-   Simple Snake flavor of tree transformers (i.e. renderers) are removed and no longer exists.
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
