# Python Authoring Mode Tutorial

```eval_rst
.. todo:: 

   Tutorial is coming soon.
```

## API Reference

The following class implements a standard parser which
comes with Paxter package library.

```eval_rst
.. autoclass:: paxter.pyauthor.RenderContext
   :members: input_text, env, tree
```

The following function creates a pre-defined unsafe Python environment dictionary to be used with the rendering context class.

```eval_rst
.. autofunction:: paxter.pyauthor.create_unsafe_env
```

Here are the functions readily available within the default environment
from the function above

```eval_rst
.. autofunction:: paxter.pyauthor.funcs.flatten
```
