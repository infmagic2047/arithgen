"""Command line program for arithgen."""

import argparse
import sys

from arithgen import __version__
from arithgen.generator import generate


def parse_args(argv):
    """Parse command line arguments for arithgen."""
    parser = argparse.ArgumentParser(
        prog='arithgen',
        description='Arithmetic expression generator',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        add_help=False,
    )
    parser.add_argument(
        '-h', '--help', action='help',
        help='Show this help message and exit.',
    )
    parser.add_argument(
        '-V', '--version', action='version',
        version='%(prog)s ' + __version__,
        help="Show program's version number and exit.",
    )
    parser.add_argument(
        '-n', '--count', type=int, default=1,
        help='Specify how many expressions to generate.',
    )
    parser.add_argument(
        '-d', '--difficulty', type=int, default=3,
        help='Specify complexity of expressions.',
    )
    parser.add_argument(
        '-F', '--format', default='{expr} = {result}',
        help='Specify output format.',
    )
    return parser.parse_args(argv)


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    args = parse_args(argv)
    for _ in range(args.count):
        expr, result = generate(difficulty=args.difficulty)
        print(args.format.format(expr=expr, result=result))
