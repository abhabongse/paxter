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
except Exception:
    metadata = {}

__author__ = metadata.get('author')
__version__ = metadata.get('version')
__status__ = metadata.get('status')
__license__ = metadata.get('license')
__maintainers__ = metadata.get('maintainers')
