#  __  __       _         __ _ _
# |  \/  | __ _| | _____ / _(_) | ___
# | |\/| |/ _` | |/ / _ \ |_| | |/ _ \
# | |  | | (_| |   <  __/  _| | |  __/
# |_|  |_|\__,_|_|\_\___|_| |_|_|\___|
#
#############################
## USER CONFIGURABLE SECTIONS
#############################

# List of written python packages
PYTHON_PROJECT_PACKAGES := paxter

# Locations to all requirement files that requires pinning down
REQUIREMENTS_FILES := $(patsubst ./%.in,%.txt,$(shell find . -type f -name '*requirements.in'))

# Location to HTML documentation build
HTML_DOC_OUTPUT = build/docs

##########
## RECIPES
##########

# This function computes a list of dependent *requirements.txt files
# from *requirements.in file.
# Usage: $(call CONSTRAINED_REQFILES,<requirements.in>)
CONSTRAINED_REQFILES = \
	$(foreach req_file, \
		$(shell grep -oP '(?<=^-c\s).*' $(1) | sed 's/\s\+//g'), \
		$(join $(dir $(1)),$(req_file)) \
	)

.PHONY: help
help:
	@# Show this help message
	@sed -n 'x;G;/^[^\S:]\+:.*\n\s*@#.*$$/{s/^\([^\S:]\+\):.*\n\s*@#\s*\(.\+\)$$/  \1 :: \2/;p;b};g;/^##@/{s/^##@\s*\(.*\)/'"\1"'/;p}' $(MAKEFILE_LIST) \
		| awk -F' :: ' 'BEGIN { printf "Usage: make \033[0;96m<target>\033[0m\n" } /^ / { printf "\033[0;96m%-30s\033[0m %s\n", $$1, $$2 } /^[^ ]/ { printf "\n\033[1m%s\033[0m\n", $$0 }'

################################
##@ Python Dependency Management
################################

.PHONY: install_python_packages
install_python_packages: $(REQUIREMENTS_FILES)
	@# Install python packages in current virtual environment
ifndef VIRTUAL_ENV
	$(error must run target inside python virtualenv)
endif
	@which pip-sync >/dev/null 2>&1 || pip install pip-tools
	pip-sync $(REQUIREMENTS_FILES)
	pip install -e .[extras]

.PHONY: lock_python_requirements
lock_python_requirements: $(REQUIREMENTS_FILES)
	@# Pin down python package dependencies as *-requirements.txt files

# NOTE: another second expansion prerequisites at the bottom of this Makefile
$(REQUIREMENTS_FILES): %.txt: %.in
ifndef VIRTUAL_ENV
	$(error must run target inside python virtualenv)
endif
	@which pip-compile >/dev/null 2>&1 || pip install pip-tools
	pip-compile -o $@ $< $(ARGS)
	@echo "Generated $@ from $^"

######################
##@ Code Quality Tools
######################

.PHONY: test
test: flake8 pytest tox_python tox_sanity
	@# Run all code quality tools

.PHONY: pytest
pytest:
	@# Run python unit tests (you may also specify ARGS='<pytest args>')
ifndef VIRTUAL_ENV
	$(error must run target inside python virtualenv)
endif
	python -m pytest -v $(ARGS)

.PHONY: pytest_cov
pytest_cov:
	@# Run python unit tests with code coverage summary
ifndef VIRTUAL_ENV
	$(error must run target inside python virtualenv)
endif
	python -m pytest $(foreach pkg,$(PYTHON_PROJECT_PACKAGES),"--cov=$(pkg)") \
		--cov-report=term-missing -v $(ARGS)

.PHONY: tox_python
tox_python:
	@# Run pytest on various python versions
ifndef VIRTUAL_ENV
	$(error must run target inside python virtualenv)
endif
	tox -e py37 -e py38

.PHONY: tox_sanity
tox_sanity:
	@# Perform other package sanity checks
	tox -e check

.PHONY: flake8
flake8:
	@# Run flake8 python code linter tool
ifndef VIRTUAL_ENV
	$(error must run target inside python virtualenv)
endif
	flake8 src tests setup.py

.PHONY: mypy
mypy:
	@# Run python type checker tool
ifndef VIRTUAL_ENV
	$(error must run target inside python virtualenv)
endif
	mypy .

.PHONY: test_clean
test_clean:
	@# Clear all cached data resulted from testing
ifndef VIRTUAL_ENV
	$(error must run target inside python virtualenv)
endif
	find . -name '.*_cache' -type d | xargs rm -rf
	find . -name '*.egg-info' -type d | xargs rm -rf
	coverage erase

.PHONY: test_clean_totally
test_clean_totally: test_clean
	@# Clear all cached data resulted from testing (including tox)
ifndef VIRTUAL_ENV
	$(error must run target inside python virtualenv)
endif
	rm -rf .tox

########################
##@ Package Distribution
########################

.PHONY: pkg_build
pkg_build:
	@# Compile package into distributable files such as wheels
ifndef VIRTUAL_ENV
	$(error must run target inside python virtualenv)
endif
	python setup.py sdist bdist_wheel

.PHONY: pkg_upload
pkg_upload:
	@# Upload compiled packages to PyPI
ifndef VIRTUAL_ENV
	$(error must run target inside python virtualenv)
endif
	twine upload dist/*

.PHONY: pkg_clean
pkg_clean:
	@# Clean compiled packages
	rm -rf build/bdist.* build/lib dist/
	find . -name '*.egg-info' -type d | xargs rm -rf
	-rmdir build

#############################
##@ Documentation Generations
#############################

.PHONY: doc_preview
doc_preview:
	@# Preview documentation generated from source code
ifndef VIRTUAL_ENV
	$(error must run target inside python virtualenv)
endif
	pdoc --template-dir docs/templates --http : $(PYTHON_PROJECT_PACKAGES)

.PHONY: doc_build
doc_build:
	@# Build document as HTML files
ifndef VIRTUAL_ENV
	$(error must run target inside python virtualenv)
endif
	pdoc --template-dir docs/templates --html --output-dir "$(HTML_DOC_OUTPUT)" \
		$(PYTHON_PROJECT_PACKAGES)
	@echo "HTML files are generated inside build/html directory."

.PHONY: doc_clean
doc_clean:
	@# Clean up generated HTML files
	rm -rf "$(HTML_DOC_OUTPUT)"
	-rmdir build

#####################
##@ Program Shortcuts
#####################

.PHONY: git_show_tree
git_show_tree:
	@# Show git commit history as a nice tree
	@git log --graph --abbrev-commit --decorate --all \
		--format=format:'%C(bold blue)%h%C(reset) - %C(bold cyan)%aD%C(reset) %C(bold green)(%ar)%C(reset)%C(bold yellow)%d%C(reset)%n''          %C(white)%s%C(reset) %C(dim white)- %an%C(reset)'

.PHONY: jnb
jnb:
	@# Launch jupyter notebook inside environment
ifndef VIRTUAL_ENV
	$(error must run target inside python virtualenv)
endif
	jupyter notebook

.PHONY: jc
jc:
	@# Launch jupyter console inside environment
ifndef VIRTUAL_ENV
	$(error must run target inside python virtualenv)
endif
	jupyter console

###################
## SECOND EXPANSION
###################

.SECONDEXPANSION:
$(REQUIREMENTS_FILES): %.txt: $$(call CONSTRAINED_REQFILES,$$<)
