# Changelog

## 0.2.0 (12 March 2020)

-   Optimized parser (remove redundant steps, refactor code, etc.)
-   Package reorganization (e.g. flavored tree transformers now in `paxter.flavors`)
-   **Simple Snake** behavior changes:
    -    A line ending with backslash will remove the backslash itself along with the newline character next to it
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
