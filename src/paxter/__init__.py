"""
Document-first text pre-processing mini-language.

## Dependencies

There are no required python package dependencies for
the core functionality of Paxter document pre-processing language.
However, extra features of Paxter requires other optional packages
from `"requirements.txt"` to be installed.


## Command Line Usage

An example command-line usage for this package would be:

```bash
$ python -m paxter
```

To see help messages, use the following command:
```bash
$ python -m paxter --help
```
"""
import json
import os

__all__ = []

this_dir = os.path.dirname(os.path.abspath(__file__))
metadata_file = os.path.join(this_dir, 'metadata.json')

try:
    with open(metadata_file) as fobj:
        metadata = json.load(fobj)

    __author__ = metadata['author']
    __version__ = metadata['version']
    __status__ = metadata['beta']
    __license__ = metadata['license']
    __maintainers__ = metadata['maintainers']

except Exception:
    pass
