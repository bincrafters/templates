#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import argparse
import logging
import pathlib
import sys

from . import __version__
from .bincrafters_templates import generate_project, InvalidArgumentError


def logging_init(verbose: bool=False):
    format = '[%(levelname)s]\t%(asctime)s %(message)s'
    level = logging.DEBUG if verbose else logging.WARNING
    logging.basicConfig(level=level, format=format, datefmt='%Y-%m-%d %H:%M:%S')


def main(args=None):
    parser = argparse.ArgumentParser()
    type_group = parser.add_argument_group("Template types")
    type_mutex_group = type_group.add_mutually_exclusive_group()
    type_mutex_group.add_argument("--default", dest="template_type", action="store_const", const="default",
                       help="Use default template type")
    type_mutex_group.add_argument("--header_only", dest="template_type", action="store_const", const="header_only",
                       help="Use header_only project type")
    type_mutex_group.add_argument("--installer_only", dest="template_type", action="store_const", const="installer_only",
                       help="Use installer_only project type")
    parser.set_defaults(template_type="default")
    output_group = parser.add_argument_group("Output options")
    output_group.add_argument("--output", "-o", type=pathlib.Path, default=pathlib.Path(),
                        help="Directory to copy the template to (default = working directory)")
    output_group.add_argument("--name", "-n", default="conan-libname",
                        help="Name of the template directory")
    parser.add_argument("--verbose", "-v", action="store_true", dest="verbose",
                        help="Verbose output")
    parser.add_argument('--version', '-V', action='version', version='%(prog)s {}'.format(__version__))
    ns = parser.parse_args(args)

    logging_init(ns.verbose)

    try:
        generate_project(template_type=ns.template_type, output=ns.output, name=ns.name)
    except InvalidArgumentError as e:
        print("An error occured", file=sys.stderr)
        print(e.args[0], file=sys.stderr)


if __name__ == "__main__":
    main()
