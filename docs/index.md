# Welcome to Paxter's documentation!

**Paxter** is a document-first, text pre-processing mini-language toolchain,
_loosely_ inspired by [@-expressions in Racket](https://docs.racket-lang.org/scribble/reader.html).

-   The Paxter library package defines the syntax for **Paxter language**
    and provides a toolchain for parsing input texts
    written in Paxter language into _an intermediate parsed tree_.
-   However, the semantics of Paxter language is left unspecified,
    meaning that users of the library have all the freedom to do
    whatever they like to render or transform the intermediate parsed tree
    into a final output they wish to achieve.  
-   Alternatively, instead of implementing an interpreter 
    for intermediate parsed tree by themselves,
    users may opt-in to utilize a preset _parsed tree renderers_,
    also provided by this library package.


## Contents

- [Getting Started](getting_started.rst)
- [Paxter Language Tutorial](paxter_language_tutorial.md)
- [Python Authoring Mode Tutorial](python_authoring_mode_tutorial.md)
- [Custom Renderer Tutorial](custom_renderer_tutorial.md)
- [Syntax Reference](syntax.rst)
- [Core API Reference](core_api.md)


## Indices and tables

- ```eval_rst
  :ref:`genindex`
  ```
- ```eval_rst
  :ref:`search`
  ```
