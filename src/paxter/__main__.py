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
    Runs Paxter parser on input text from INPUT_FILE and write to OUTPUT_FILE.
    """
    from paxter.core import ParseContext

    tree = ParseContext(input_file.read()).parse()
    output_file.write(repr(tree))
    output_file.write("\n")


@program.command()
@click.option('-i', '--input-file', type=click.File(mode='r'), default='-',
              help="Path to input file ('-' for stdin)")
@click.option('-o', '--output-file', type=click.File(mode='w'), default='-',
              help="Path to output file ('-' for stdout)")
@click.option('-e', '--env-file',
              type=click.Path(exists=True, dir_okay=False, readable=True),
              help="Path to python file to extract the environment.")
def python_authoring(input_file, output_file, env_file):
    """
    Runs Paxter parser followed by Unsafe Python renderer
    in order to render input text from INPUT_FILE
    and write the output result to OUTPUT_FILE.
    """
    import runpy
    from paxter.core import ParseContext
    from paxter.renderers.python import (
        RenderContext, create_unsafe_env, flatten,
    )

    input_text = input_file.read()
    tree = ParseContext(input_text).parse()
    env = create_unsafe_env(runpy.run_path(env_file) if env_file else {})
    output_text = flatten(RenderContext(input_text, env).visit_fragment(tree))

    output_file.write(output_text)


if __name__ == '__main__':
    program()
