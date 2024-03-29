"""
Running CLI commands.
"""
from __future__ import annotations

import click


@click.group()
def program():
    pass


def input_output_options(func):
    func = click.option(
        '-o', '--output-file',
        type=click.File(mode='w'),
        default='-',
        help="Path to output file ('-' for stdout)",
    )(func)
    func = click.option(
        '-i', '--input-file',
        type=click.File(mode='r'),
        default='-',
        help="Path to input file ('-' for stdin)",
    )(func)
    return func


@program.command(name='syntax')
@input_output_options
def run_parse(input_file, output_file):
    """
    Parses the input text into Paxter parsed tree.

    It reads input text from INPUT_FILE
    and writes the parsed tree to OUTPUT_FILE.

    Transform: input text -> parsed tree
    """
    from paxter.syntax import parse

    src_text = input_file.read()
    parsed_tree = parse(src_text)

    output_file.write(repr(parsed_tree))
    output_file.write("\n")


@program.command(name='document')
@input_output_options
@click.option('-e', '--env-file',
              type=click.Path(exists=True, dir_okay=False, readable=True),
              help="Path to python file to extract the environment.")
def run_document(input_file, output_file, env_file):
    """
    Evaluates the input text into the document object.

    It reads input text from INPUT_FILE and pass it through the syntax.
    Then the parsed tree is evaluated into document object
    using the environment provided by the
    paxter.quickauthor supplementary subpackage.
    Finally, the document object structure is written to OUTPUT_FILE.

    Transform: input text -> parsed tree -> document object
    """
    import runpy
    from paxter.quickauthor import run_document_paxter, create_document_env

    src_text = input_file.read()
    env = create_document_env(runpy.run_path(env_file) if env_file else {})
    document = run_document_paxter(src_text, env)

    output_file.write(repr(document))
    output_file.write("\n")


@program.command(name='html')
@input_output_options
@click.option('-e', '--env-file',
              type=click.Path(exists=True, dir_okay=False, readable=True),
              help="Path to python file to extract the environment.")
def run_html(input_file, output_file, env_file):
    """
    Parses, evaluates, and renders the final HTML output.

    It reads input text from INPUT_FILE and pass it through the syntax.
    Then the parsed tree is evaluated into document object
    using the environment provided by the
    paxter.quickauthor supplementary subpackage.
    Finally, the document object is rendered to HTML output
    which gets written to OUTPUT_FILE.

    Transform: input text -> parsed tree -> document object -> html string
    """
    import runpy
    from paxter.quickauthor import run_document_paxter, create_document_env

    src_text = input_file.read()
    env = create_document_env(runpy.run_path(env_file) if env_file else {})
    document = run_document_paxter(src_text, env)

    output_file.write(document.html())
    output_file.write("\n")


if __name__ == '__main__':
    program()
