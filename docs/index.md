# Welcome to Paxter's documentation!

**Paxter** is a document-first, text pre-processing mini-language toolchain,
_loosely_ inspired by [@-expressions in Racket](https://docs.racket-lang.org/scribble/reader.html).

-   The Paxter library package mainly provides a toolchain for 
    parsing an input text (written in **Paxter language**) 
    into _an intermediate parsed tree_.
-   However, the Paxter toolchain **does not specify** how 
    the parsed tree should be interpreted or rendered into final result.
    Users of the Paxter library have all the freedom to do
    whatever they like to transform the intermediate result
    into a final output result they wish to achieve.  
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
