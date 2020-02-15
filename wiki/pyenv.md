# Setup Python Environment

When starting a new python project, we recommend using the latest version of python 
(which is `python3.8` at the time of this writing).
However, some python package may not yet be supported with the latest version
of python so please beware.

It is likely that the system-installation of python might not be the most recent one,
so we recommend using [`pyenv`](https://github.com/pyenv/pyenv#installation)
to install the version of python you desired 
(see [detailed instructions below](#detailed-instructions)).

Once the desired version of python is installed,
then use it to create the `virtualenv` for the project.


## Detailed Instructions

Here is the recommended method for Linux distributions:

1. Install `pyenv` with [`pyenv-installer`](https://github.com/pyenv/pyenv-installer).
   Carefully follow the instructions given, 
   which includes adding `pyenv` bin directories to `$PATH`.
   
   _This step is to be completed just one per local development machine._

2. Install the desired version of python using the following command 
   (assuming version `3.8.1` is used here):
   ```bash
   $ pyenv install 3.8.1
   ```
   - If `pyenv` command is not present, perhaps try restarting the machine first.
   - If there are other problems while installing, 
     [consult the troubleshoot page](https://github.com/pyenv/pyenv/wiki/common-build-problems).

3. Determine the specific location of python binary.
   For example, continuing from the previous step,
   the location of python 3.8.1 binary should be:
   ```bash
   $ echo "$(pyenv prefix 3.8.1)/bin/python"
   /home/user/.pyenv/versions/3.8.1/bin/python
   ```

   Perhaps verify that it is indeed a python binary before continue.
   ```bash
   $ "$(pyenv prefix 3.8.1)/bin/python"
   Python 3.8.1 (default, Dec 24 2019, 15:17:29) 
   [GCC 7.4.0] on linux
   Type "help", "copyright", "credits" or "license" for more information.
   >>> 
   ```

4. Create a new virtualenv using the path to python binary found in previous step:
   ```bash
   # virtualenv --python "$(pyenv prefix 3.8.1)/bin/python" venv
   ```
   With the above command, a new directory called `venv` will be created
   and it will bind to the python binary as provided.

5. Before starting development, do not forget to enter the `virtualenv`:
   ```bash
   $ source venv/bin/activate
   ```
   It is guaranteed that the correct version of python (previously bound) will be used.
   This step is required before using some particular commands from `Makefile`;
   `Makefile` will explicitly check that you have activated the `virtualenv` first 
   to avoid unintentionally using the system-installation of python.
