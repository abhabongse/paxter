import click

from myhelpers.dummy import longest_common_prefix


@click.command()
@click.argument('fst', metavar='STRING')
@click.argument('snd', metavar='STRING')
def program(fst, snd):
    """
    Computes the longest common prefix of both STRINGs.
    """
    result = longest_common_prefix(fst, snd)
    print(result)


program()
