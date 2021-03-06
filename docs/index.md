# Paxter Documentation

**Paxter language** helps users write rich-formatting documents
with simple and easy-to-understand syntax.
Nevertheless, users still have access to the python environment:
they can call python functions and evaluate python expressions
right inside the document itself,
giving users flexibility and power to customize 
their approach to writing documents.

**Paxter package** is a document-first, text processing language toolchain,
inspired by [@-expressions in Racket](https://docs.racket-lang.org/scribble/reader.html).
Users of the package also has the access to the Paxter language parser API
which allows them to implement new interpreters on top of the Paxter language
if they so wish.


## Site Contents

```{toctree}
---
caption: Beginner Tutorials
maxdepth: 2
---
tutorials/beginner/getting-started
tutorials/beginner/quick-blogging
tutorials/beginner/evaluation-cycle-explained
tutorials/beginner/interpreting-python-code
tutorials/beginner/disable-python-environment-demo
tutorials/beginner/escaping-mechanisms
tutorials/beginner/dive-into-command-syntax
tutorials/beginner/codeblock-syntax-highlight-demo
```

```{toctree}
---
caption: Intermediate Tutorials
maxdepth: 2
---
tutorials/intermediate/index
```

```{toctree}
---
caption: API References
maxdepth: 1
---
references/core-api
references/authoring-api
references/syntax
```

```{toctree}
---
caption: Legacy Documentation
maxdepth: 1
---
legacy/getting_started
legacy/paxter_language_tutorial
legacy/python_authoring_mode_tutorial
```


## Indices and tables

- {ref}`genindex`
- {ref}`search`
