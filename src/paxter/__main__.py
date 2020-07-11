"""
Running CLI commands.
"""
import click


@click.group()
def program():
    pass


@program.command()
@click.option('-i', '--input-file', type=click.File(mode='r'), default='-',
              help="Path to input file ('-' for stdin)")
@click.option('-o', '--output-file', type=click.File(mode='w'), default='-',
              help="Path to output file ('-' for stdout)")
@click.option('-s', '--switch', default='@', show_default=True, metavar='SWITCH',
              help="Paxter expression switch symbol character")
def parse(input_file, output_file, switch):
    """
    Runs only the parser on the input.
    It reads input text from INPUT_FILE
    and writes the parsed tree to OUTPUT_FILE.
    """
    from paxter.core import ParseContext

    tree = ParseContext(input_file.read()).tree
    output_file.write(repr(tree))
    output_file.write("\n")


@program.command()
@click.option('-i', '--input-file', type=click.File(mode='r'), default='-',
              help="Path to input file ('-' for stdin)")
@click.option('-o', '--output-file', type=click.File(mode='w'), default='-',
              help="Path to output file ('-' for stdout)")
@click.option('-e', '--env-file',
              type=click.Path(exists=True, dir_okay=False, readable=True),
              help="Path to pyauthor file to extract the environment.")
def pyauthor_string(input_file, output_file, env_file):
    """
    Python authoring bare mode: run the parser with a Python renderer.
    It reads input text from INPUT_FILE and pass it through the parser.
    Then the parsed tree is transformed into the final result
    using the unsafe Python renderer, and output to OUTPUT_FILE.
    """
    import runpy
    from paxter.core import ParseContext
    from paxter.pyauthor import StringRenderContext, create_unsafe_bare_env

    input_text = input_file.read()
    tree = ParseContext(input_text).tree
    env = create_unsafe_bare_env(runpy.run_path(env_file) if env_file else {})
    output = StringRenderContext(input_text, env, tree).rendered
    output_file.write(output)


@program.command()
@click.option('-i', '--input-file', type=click.File(mode='r'), default='-',
              help="Path to input file ('-' for stdin)")
@click.option('-o', '--output-file', type=click.File(mode='w'), default='-',
              help="Path to output file ('-' for stdout)")
@click.option('-e', '--env-file',
              type=click.Path(exists=True, dir_okay=False, readable=True),
              help="Path to pyauthor file to extract the environment.")
def pyauthor_document(input_file, output_file, env_file):
    """
    Python authoring document mode: run the parser with a Python renderer.
    It reads input text from INPUT_FILE and pass it through the parser.
    Then the parsed tree is transformed into the final result
    using the unsafe Python renderer, and output to OUTPUT_FILE.
    """
    import runpy
    from paxter.core import ParseContext
    from paxter.pyauthor import DocumentRenderContext, create_unsafe_document_env

    input_text = input_file.read()
    tree = ParseContext(input_text).tree
    env = create_unsafe_document_env(runpy.run_path(env_file) if env_file else {})
    output = DocumentRenderContext(input_text, env, tree).rendered
    output_file.write(str(output))


if __name__ == '__main__':
    program()
