"""
Collection of command-line commands.
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
    Runs Paxter parser on input from INPUT_FILE and write to OUTPUT_FILE.
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
@click.option('-s', '--switch', default='@', show_default=True, metavar='SWITCH',
              help="Paxter expression switch symbol character")
def render_simple_python(input_file, output_file, switch):
    """
    Runs Paxter parser and simple python transformer
    on input from INPUT_FILE and write to OUTPUT_FILE.
    """
    from paxter.core import Parser, Lexer, SimplePythonTransformer
    lexer = Lexer(switch=switch)
    parser = Parser(lexer=lexer)
    transformer = SimplePythonTransformer()

    parsed_tree = parser.parse(input_file.read())
    _, result = transformer.transform({}, parsed_tree)
    output_file.write(result)
