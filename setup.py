import os
import re
from setuptools import find_packages, setup


def read_file(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def get_version():
    content = read_file('arithgen/__init__.py')
    regex = r'^__version__ = [\'"]([^\'"]*)[\'"]$'
    match = re.search(regex, content, re.M)
    if not match:
        raise RuntimeError('Cannot find version string in __init__.py')
    return match.group(1)


setup(
    name='arithgen',
    version=get_version(),
    description='Arithmetic expression generator',
    long_description=read_file('README.rst'),
    url='https://github.com/infmagic2047/arithgen',
    author='Yutao Yuan',
    author_email='infmagic2047reg@outlook.com',
    license='MIT',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Education',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.4',
        'Topic :: Education',
        'Topic :: Games/Entertainment',
    ],
    packages=find_packages(exclude=['tests*']),
    install_requires=[
        'PyYAML',
        'docopt',
    ],
    entry_points={
        'console_scripts': [
            'arithgen = arithgen.cmdline:main',
            'arithgen-quiz = arithgen.quiz:main',
        ],
    },
    zip_safe=True,
)
