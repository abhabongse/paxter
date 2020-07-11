"""
Running CLI commands.
"""
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


@program.command()
@input_output_options
def parse(input_file, output_file):
    """
    Runs only the parser on the input.
    It reads input text from INPUT_FILE
    and writes the parsed tree to OUTPUT_FILE.
    """
    from paxter.core import ParseContext

    input_text = input_file.read()
    tree = ParseContext(input_text).tree
    output_file.write(repr(tree))
    output_file.write("\n")


@program.command()
@input_output_options
@click.option('-e', '--env-file',
              type=click.Path(exists=True, dir_okay=False, readable=True),
              help="Path to pyauthor file to extract the environment.")
def pyauthor_string(input_file, output_file, env_file):
    """
    Python string authoring mode: run the parser followed by a Python renderer.
    It reads input text from INPUT_FILE and pass it through the parser.
    Then the parsed tree is transformed into the final string result
    using the string Python renderer, and output to OUTPUT_FILE.
    """
    import runpy
    from paxter.core import ParseContext
    from paxter.pyauthor import StringRenderContext, create_unsafe_bare_env

    input_text = input_file.read()
    tree = ParseContext(input_text).tree
    env = create_unsafe_bare_env(runpy.run_path(env_file) if env_file else {})
    string_output = StringRenderContext(input_text, env, tree).rendered
    output_file.write(string_output)
    output_file.write("\n")


@program.command()
@input_output_options
@click.option('-e', '--env-file',
              type=click.Path(exists=True, dir_okay=False, readable=True),
              help="Path to pyauthor file to extract the environment.")
def pyauthor_document(input_file, output_file, env_file):
    """
    Python document authoring mode: run the parser followed by a Python renderer.
    It reads input text from INPUT_FILE and pass it through the parser.
    Then the parsed tree is transformed into the final HTML result
    using the string Python renderer, and output to OUTPUT_FILE.
    """
    import runpy
    from paxter.core import ParseContext
    from paxter.pyauthor import DocumentRenderContext, create_unsafe_document_env

    input_text = input_file.read()
    tree = ParseContext(input_text).tree
    env = create_unsafe_document_env(runpy.run_path(env_file) if env_file else {})
    document_output = DocumentRenderContext(input_text, env, tree).rendered
    rendered_html = document_output.render_html()
    output_file.write(rendered_html)
    output_file.write("\n")


if __name__ == '__main__':
    program()
