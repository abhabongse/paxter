import click

from paxter.parser import Paxter


@click.command()
@click.option('-i', '--input-file', type=click.File(mode='r'), default='-',
              help="Path to input file ('-' for stdin)")
@click.option('-o', '--output-file', type=click.File(mode='w'), default='-',
              help="Path to output file ('-' for stdout)")
def program(input_file, output_file):
    """
    Runs Paxter parser on input from INPUT_FILE and write to OUTPUT_FILE.
    """
    parsed_tree = Paxter.parse(input_file.read())
    output_file.write(repr(parsed_tree))
    output_file.write("\n")


program()
