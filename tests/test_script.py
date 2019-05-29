# -*- coding: utf-8 -*-

from bincrafters_templates.__main__ import main as bincrafters_template_main
import os
from tests import conan


def test_main_valid_args(tmpdir, conan):
    outputpath = tmpdir.strpath
    name = "conan-test_main_lib"
    args = ["-o", outputpath, "--default", "-n", name]

    bincrafters_template_main(args)

    conanfile_path = os.path.join(outputpath, name, "conanfile.py")

    answer = conan.inspect(conanfile_path, ("settings", "options", ))

    assert answer["settings"] is not None
    assert answer["options"] is not None

    assert "os" in answer["settings"]
    assert "arch" in answer["settings"]


def test_main_invalid_args(tmpdir, conan, capsys):
    outputpath = tmpdir.strpath
    name = "conan-test_main_lib"
    os.mkdir(os.path.join(outputpath, name))
    args = ["-o", outputpath, "--default", "-n", ""]

    bincrafters_template_main(args)

    captured = capsys.readouterr()
    assert "error occured" in captured.err
