"""
Collection of CLI commands.
"""
import click  # pragma: no cover


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
    Runs Paxter parser on input text from INPUT_FILE and write to OUTPUT_FILE.
    """
    from paxter.core import Parser, Lexer
    lexer = Lexer(switch=switch)
    parser = Parser(lexer=lexer)

    parsed_tree = parser.parse(input_file.read())
    output_file.write(repr(parsed_tree))
    output_file.write("\n")


@program.command()
@click.option('-i', '--input-file', type=click.File(mode='r'), default='-',
              help="Path to input file ('-' for stdin)")
@click.option('-o', '--output-file', type=click.File(mode='w'), default='-',
              help="Path to output file ('-' for stdout)")
@click.option('-e', '--env-file',
              type=click.Path(exists=True, dir_okay=False, readable=True),
              help="Path to python file to extract the environment.")
@click.option('-s', '--switch', default='@', metavar='SWITCH', show_default=True,
              help="Paxter expression switch symbol character")
def simple_snake(input_file, output_file, env_file, switch):
    """
    Runs Paxter parser and "Simple Snake" transformer
    in order to render input text from INPUT_FILE
    and write the output result to OUTPUT_FILE.
    """
    import runpy
    from paxter.core import Parser, Lexer
    from paxter.flavors.simple_snake.transformer import SimpleSnakeTransformer

    lexer = Lexer(switch=switch)
    parser = Parser(lexer=lexer)
    transformer = SimpleSnakeTransformer()

    # Parse input text
    tree = parser.parse(input_file.read())

    # Read environment from file if exists
    env = runpy.run_path(env_file) if env_file else {}

    # Transform the tree into output text
    _, output_text = transformer.transform(env, tree)
    output_file.write(output_text)
