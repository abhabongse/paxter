#!/usr/bin/env python3
"""
Small program which provides playground to a program written for Lark.
Author: Abhabongse Janthong
"""
import argparse
import cmd

from lark import Lark


def load_lark_grammar(filename: str) -> Lark:
    """
    Load a grammar written in Lark from a given filename.
    """
    with open(filename) as fobj:
        grammar_text = fobj.read()
    return Lark(grammar_text, debug=True)


def parse_arguments(args=None):
    """
    Parse a given list of program arguments.
    By default, the input program arguments from sys.argv is used.
    """
    parser = argparse.ArgumentParser(description="Load lark grammar and run.")
    parser.add_argument('grammar_file', help="Path to grammar file")
    return parser.parse_args(args)


class REPLShell(cmd.Cmd):
    intro = "Welcome to the grammar test shell.  Type help of ? to list commands.\n"
    prompt = "(lark) "
    lark_grammar: Lark

    def __init__(self, lark_grammar: Lark):
        self.lark_grammar = lark_grammar
        super().__init__()

    def do_parse(self, arg):
        try:
            result = self.lark_grammar.parse(arg)
            print(result.pretty())
        except Exception as exc:
            print("Exception:", exc)
            print(f"You typed: {arg!r}")

    def do_EOF(self, arg):
        return True

    def postcmd(self, stop, line):
        print()
        return stop

    def postloop(self):
        print("\nBye!")


if __name__ == "__main__":
    args = parse_arguments()
    lark_grammar = load_lark_grammar(args.grammar_file)
    REPLShell(lark_grammar).cmdloop()
