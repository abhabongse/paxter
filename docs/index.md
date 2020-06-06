# Welcome to Paxter's documentation!

Paxter is a document-first text pre-processing mini-language, _loosely_ inspired by
[@-expressions in Racket](https://docs.racket-lang.org/scribble/reader.html).  

-   The language mainly provides a toolchain to parse an input text into a document tree
    ([similarly to a DOM](https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model/Introduction)).

-   However, the language itself **does not specify** how the parsed tree 
    will be transformed into the final rendered output text.
    Users have all the freedom to interpret or render the document tree 
    into an output format however they like.

-   Alternatively, instead of implementing a document tree renderer by themselves, 
    users may opt-in to use pre-defined **renderers** of document tree renderers 
    also provided by this package. 

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
