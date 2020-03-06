# Contributing

Contributions are welcome, and they are greatly appreciated\! Every
little bit helps, and credit will always be given.

## Bug reports

When [reporting a bug](https://github.com/abhabongse/paxter/issues)
please include:

>   - Your operating system name and version.
>   - Any details about your local setup that might be helpful in
>     troubleshooting.
>   - Detailed steps to reproduce the bug.

## Documentation improvements

Paxter could always use more documentation, whether as part of the
official Paxter docs, in docstrings, or even on the web in blog posts,
articles, and such.

## Feature requests and feedback

The best way to send feedback is to file an issue at
<https://github.com/abhabongse/paxter/issues>.

If you are proposing a feature:

  - Explain in detail how it would work.
  - Keep the scope as narrow as possible, to make it easier to
    implement.
  - Remember that this is a volunteer-driven project, and that code
    contributions are welcome :)

## Development

To set up <span class="title-ref">paxter</span> for local development:

1.  Fork [paxter](https://github.com/abhabongse/paxter) (look for the
    "Fork" button).

2.  Clone your fork locally:

        git clone git@github.com:abhabongse/paxter.git

3.  Create a branch for local development:

        git checkout -b name-of-your-bugfix-or-feature

    Now you can make your changes locally.

4.  When you're done making changes run all the checks and docs builder
    with [tox](https://tox.readthedocs.io/en/latest/install.html) one
    command:

        tox

5.  Commit your changes and push your branch to GitHub:

        git add .
        git commit -m "Your detailed description of your changes."
        git push origin name-of-your-bugfix-or-feature

6.  Submit a pull request through the GitHub website.

### Pull Request Guidelines

If you need some code review or feedback while you're developing the
code just make the pull request.

For merging, you should:

1.  Include passing tests (run `tox`)\[1\].
2.  Update documentation when there's new API, functionality etc.
3.  Add a note to `CHANGELOG.md` about the changes.
4.  Add yourself to `AUTHORS.md`.

### Tips

To run a subset of tests:

    tox -e envname -- pytest -k test_myfeature

To run all the test environments in *parallel* (you need to `pip install
detox`):

    detox

1.  If you don't have all the necessary python versions available
    locally you can rely on Travis - it will [run the
    tests](https://travis-ci.org/abhabongse/paxter/pull_requests) for
    each change you add in the pull request.

    It will be slower though ...
