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
    from paxter.parser import ParseContext

    input_text = input_file.read()
    parse_context = ParseContext(input_text)

    output_file.write(repr(parse_context.tree))
    output_file.write("\n")


@program.command()
@input_output_options
@click.option('-e', '--env-file',
              type=click.Path(exists=True, dir_okay=False, readable=True),
              help="Path to pyauthor file to extract the environment.")
def html(input_file, output_file, env_file):
    """
    Parses and evaluates the input text as HTML document.
    It reads input text from INPUT_FILE and pass it through the parser.
    Then the parsed tree is transformed into the final HTML result
    using the string Python renderer, and output to OUTPUT_FILE.
    """
    import runpy
    from paxter.authoring import run_document_paxter, create_document_env

    input_text = input_file.read()
    env = create_document_env(runpy.run_path(env_file) if env_file else {})
    document = run_document_paxter(input_text, env)

    output_file.write(document.html())
    output_file.write("\n")


if __name__ == '__main__':
    program()
