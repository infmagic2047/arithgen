"""Quiz mode of arithgen.

Usage:
    arithgen-quiz [options]
    arithgen-quiz --help
    arithgen-quiz --version

Options:
    -d, --difficulty=<difficulty>  Specify the complexity of
                                   expressions. [default: 3]
    -F, --format=<format>          Specify the output format.
                                   [default: {expr}]
    -r, --strict                   Only accept answer with an integer or
                                   a fraction in the form of a/b with
                                   gcd(a, b) == 1 and b > 1. By default
                                   anything accepted by Fraction
                                   constructor is OK.
    -s, --silent                   Suppress summary information output.

"""

import collections
import os
import re
import sys
from fractions import Fraction, gcd

import yaml
from docopt import docopt

from arithgen import __version__
from arithgen.generator import generate


def update_recursive(orig_dict, new_dict):
    """Update dict orig_dict with new_dict recursively."""
    for key, val in new_dict.items():
        if isinstance(val, collections.Mapping):
            orig_dict[key] = orig_dict.get(key, {})
            update_recursive(orig_dict[key], val)
        else:
            orig_dict[key] = val


def parse_config_files():
    xdg_config_home = os.environ.get('XDG_CONFIG_HOME',
                                     os.path.expanduser('~/.config'))
    xdg_config_dirs = ([xdg_config_home] +
                       os.environ.get('XDG_CONFIG_DIRS',
                                      '/etc/xdg').split(':'))
    config_dirs = [os.path.join(path, 'arithgen')
                   for path in xdg_config_dirs]
    config_files = [os.path.join(path, 'quiz.yaml')
                    for path in config_dirs]
    default_config = '''
        messages:
            prompt: 'Your answer? '
            correct-answer: 'Correct!'
            wrong-answer: 'Wrong answer, {user_result} != {result}'
            summary: 'Correct rate: {correct_count}/{total_count}
                ({correct_rate_percent:.2f}%)'
    '''
    config = yaml.safe_load(default_config)
    for filename in reversed(config_files):
        try:
            with open(filename, 'r') as f:
                content = f.read()
        except IOError:
            pass
        else:
            now_conf = yaml.safe_load(content)
            if now_conf is not None:
                update_recursive(config, now_conf)
    return config


def parse_fraction_strict(string):
    if string == '0':
        return Fraction(0)
    match = re.fullmatch(r'[1-9][0-9]*', string)
    if match:
        return Fraction(string)
    match = re.fullmatch(r'([1-9][0-9]*)/([1-9][0-9]*)',
                         string)
    if match:
        left = int(match.group(1))
        right = int(match.group(2))
        if gcd(left, right) == 1 and right > 1:
            return Fraction(left, right)
    raise ValueError('Format error')


def get_valid_user_input(*, prompt='', strict=False):
    """Return a valid user input as Fraction."""
    frac_converter = parse_fraction_strict if strict else Fraction
    while True:
        user_input = input(prompt)
        try:
            user_input_fraction = frac_converter(user_input)
        except (ValueError, ZeroDivisionError):
            print('Format error, please try again')
        else:
            return user_input_fraction


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    args = docopt(__doc__, argv=argv,
                  version='arithgen ' + __version__)
    try:
        difficulty = int(args['--difficulty'])
    except ValueError:
        print('Invalid arguments')
        return 1
    conf = parse_config_files()
    total_count = 0
    total_correct = 0
    while True:
        expr, result = generate(difficulty=difficulty)
        print(args['--format'].format(expr=expr))
        try:
            user_result = get_valid_user_input(
                prompt=conf['messages']['prompt'],
                strict=args['--strict'],
            )
        except EOFError:
            print('quit')
            break
        if user_result == result:
            print(conf['messages']['correct-answer'].format(
                result=result,
                user_result=user_result,
            ))
            total_correct += 1
        else:
            print(conf['messages']['wrong-answer'].format(
                result=result,
                user_result=user_result,
            ))
        total_count += 1
    if not args['--silent'] and total_count:
        correct_rate = total_correct / total_count
        print(conf['messages']['summary'].format(
            correct_rate=correct_rate,
            correct_rate_percent=correct_rate * 100,
            correct_count=total_correct,
            total_count=total_count,
        ))
