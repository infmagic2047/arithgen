"""Arithmetic expression generator.

Usage:
    arithgen [options]
    arithgen --help
    arithgen --version

Options:
    -n, --count=<count>            Specify how many expressions to
                                   generate. [default: 1]
    -d, --difficulty=<difficulty>  Specify the complexity of
                                   expressions. [default: 3]
    -F, --format=<format>          Specify the output format.
                                   [default: {expr} = {result}]

"""

import sys

from docopt import docopt

from arithgen import __version__
from arithgen.generator import generate


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    args = docopt(__doc__, argv=argv,
                  version='arithgen ' + __version__)
    try:
        count = int(args['--count'])
        difficulty = int(args['--difficulty'])
    except ValueError:
        print('Invalid arguments')
        return 1
    for _ in range(count):
        expr, result = generate(difficulty=difficulty)
        print(args['--format'].format(expr=expr, result=result))
