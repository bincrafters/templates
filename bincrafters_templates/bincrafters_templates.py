# -*- coding: utf-8 -*-

import logging
import pathlib
import shutil

TEMPLATE_PATH = pathlib.Path(__file__).absolute().parent
PROJECT_TYPES = [
    "default",
    "header_only",
    "installer_only",
]


class InvalidArgumentError(Exception):
    pass


def generate_project(template_type: str, output: pathlib.Path, name: str):
    logging.debug("generate_project(%r, %r, %r)", template_type, output, name)
    output = output.absolute()

    src_template_path = TEMPLATE_PATH / template_type
    if template_type not in PROJECT_TYPES or not src_template_path.is_dir():
        raise InvalidArgumentError("Invalid template type: {}".format(template_type))

    dst_template_path = output / name
    if dst_template_path.exists():
        raise InvalidArgumentError("Destination already exists: {}".format(str(dst_template_path)))

    logging.debug("Copying %s to %s", src_template_path, dst_template_path)
    shutil.copytree(src=src_template_path, dst=dst_template_path)

    shutil.copytree(src=TEMPLATE_PATH / ".ci", dst=dst_template_path / ".ci")

    shutil.copytree(src=TEMPLATE_PATH / ".github", dst=dst_template_path / ".github")
