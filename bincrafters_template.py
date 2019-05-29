#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import pathlib
import shutil


TEMPLATE_PATH = pathlib.Path(__file__).absolute().parent


def main():
    parser = argparse.ArgumentParser()
    type_group = parser.add_argument_group("Template types")
    type_mutex_group = type_group.add_mutually_exclusive_group()
    type_mutex_group.add_argument("--default", dest="type", action="store_const", const="default",
                       help="Use default project type")
    type_mutex_group.add_argument("--header_only", dest="type", action="store_const", const="header_only",
                       help="Use header_only project type")
    type_mutex_group.add_argument("--installer_only", dest="type", action="store_const", const="installer_only",
                       help="Use installer_only project type")
    parser.set_defaults(type="default")
    output_group = parser.add_argument_group("Output options")
    output_group.add_argument("--output", "-o", type=pathlib.Path, default=pathlib.Path(),
                        help="Directory to copy the template to (default = working directory)")
    output_group.add_argument("--name", "-n", default="conan-name",
                        help="Name of the template directory")
    args = parser.parse_args()

    shutil.copytree(src=TEMPLATE_PATH / args.type, dst=args.output / args.name)
    shutil.copytree(src=TEMPLATE_PATH / ".ci", dst=args.output / args.name / ".ci")
    shutil.copytree(src=TEMPLATE_PATH / ".github", dst=args.output / args.name / ".github")


if __name__ == "__main__":
    main()
