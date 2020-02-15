# Project Template Customization

1. Dummy python packages at project root (i.e. `myhelpers` and `mypackage`)
   can be removed, duplicated, or renamed as needed.
   Example packages at project root includes `myhelpers` and `mypackage`.
   These can be removed, duplicated, or renamed as needed.
   
   Do not forget to update the list of `PYTHON_PROJECT_PACKAGES` at project root
   at the top of `Makefile` accordingly also.
   
2. For each new python package directory, add a new `requirements.in`
   (or with the filename in the pattern of `*-requirements.in`)
   inside such directory.
   
   Note that the variable `REQUIREMENTS_FILES` at the top of `Makefile`
   should be able to pick up new `requirements.in` file automatically
   so that the corresponding `requirements.txt` can be generated at the same location.
   It is constructed using the following command in `Makefile`.
   ```
   REQUIREMENTS_FILES := $(patsubst ./%.in,%.txt,$(shell find . -type f -name '*.in'))
   ```
   Alternatively, this list can be hand written instead by using the following syntax:
   ```
   # List of written python packages
   PYTHON_PROJECT_PACKAGES := myhelpers
   PYTHON_PROJECT_PACKAGES += mypackage   
   ```

3. Edit contents of `requirements.in` files 
   to add or remove python packages as you wish.
   Then do not forget to pin down dependencies by running the following command:
   ```bash
   (venv)$ make lock_python_requirements && make install_python_packages
   ```
