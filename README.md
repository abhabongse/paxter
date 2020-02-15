# Python Project Template

Template for python project structure (with annotations).


## Features

- Works with vanilla virtualenv in order to manage the installation of 
  package package dependencies inside the local development machine.
- Development-only python package dependencies are maintained separately
  from those being used in the actual codebase
  (i.e. `dev-requirements.txt` as opposed to `requirements.txt`
  inside each root package such as `myhelpers` and `mypackage`).
- Maintains python requirements files separately for each root project package,
  hence allowing multiple docker images to be built separately
  with compacted installation of dependent python packages.
- `Makefile` for common python-related commands (such as for 
  python dependency management, testing and linting tools,
  documentation generation, etc.).
  

## Local Development Setup

1. Install a specific version of python 3 (recommended using `pyenv`)
   and use it create a new virtualenv.  
   [For more information, click here.](wiki/pyenv.md)
2. Inside the virtualenv,
   run the following to install all required python packages
   ```bash
   (venv)$ make install_python_packages
   ```

## Customization

[Read how to customize this python project template.](wiki/customize.md)


## Git Commit Checklist
​
Before committing changes in Git Repository, 
please run through the following checklist:
​
1. Run `make test` to test for code quality
   (such as `flake8` code lint, `pytest` unit tests, etc.)
   Fix any complaints until there is no error message.
2. Run `git status` to see the status of file changes.
   Verify with your eye that it is what is expected.


## Useful Makefile Commands

#### List all make commands

```bash
(venv)$ make  # or make help
```

#### Install new python packages
​
To install a new python package (or update the version of existing ones),
modify the file `requirements.in` (or `dev-requirements.in`; see FAQ)
and run the following to pin down packages and install.
```bash
(venv)$ make lock_python_requirements && make install_python_packages
```


## Frequently Asked Questions

#### What are differences between `requirements.in` and `requirements.txt`?

- `requirements.in` contains a list of python packages 
  we wish to install and use it directly.
- `requirements.txt` contains the pinned/locked down python packages
  which is the result of resolving package dependencies in `requirements.in`.

**Note:** For NodeJS programmers, an analogy for this would be `package.json`
vs `package-lock.json` files respectively.

This allows us to have _deterministic package installations_ across multiple machines,
which means that it is less likely one program works on one machine but not the other.

#### Why are there multiple `requirements.txt` files in various python local packages?

In this project template, we demonstrate how programmers could separately maintain
python package dependencies for _different_ local python packages
(i.e. we have separate [`myhelpers/requirements.txt`](myhelpers/requirements.txt) 
and [`mypackage/requirements.txt`](requirements.txt) files).
This pattern is particularly useful if programmers need to build multiple docker images,
each with separate python package dependencies with space-efficient optimizations.

#### What are differences between `requirements.txt` and `dev-requirements.txt`?

- `requirements.txt` contains a list of python packages
  explicitly used in the main codebase (via import statements).
- `dev-requirements.txt` contains a separate list of python packages
  assisting in software development process in local environment
  (but are _never_ used in the main codebase).

**Note:** For NodeJS programmers, an analogy for this would be `dependencies` 
vs `devDependencies` section in `package.json` file, respectively.

#### Why does `Makefile` not assuming a particular `virtualenv` setup?

The tasks of creating and maintaining python `virtualenv` were left to individual 
preferences of python programmers (esp. critical in collaborative projects).
`Makefile` merely enforces that programmers must enter the virtualenv
before executing the scripts as a safeguard against preventable human misuse.
