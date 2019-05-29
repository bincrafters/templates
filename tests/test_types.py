# -*- coding: utf-8 -*-

from bincrafters_templates.bincrafters_templates import PROJECT_TYPES, generate_project, InvalidArgumentError

import pathlib
import pytest
from pytest_cases import pytest_fixture_plus
from tests import conan


@pytest_fixture_plus
@pytest.mark.parametrize("template_type", PROJECT_TYPES, ids=lambda t: f"template_type:{t}")
def valid_template_type(template_type):
    return template_type


def _test_valid_template_type(template_type, outputpath, conan):
    name = "conan-testname"

    generate_project(template_type=template_type, output=outputpath, name=name)

    project_path = outputpath / name

    assert (project_path / "test_package").is_dir()
    assert (project_path / ".ci").is_dir()
    assert (project_path / ".github").is_dir()
    assert (project_path / ".gitignore").is_file()
    assert (project_path / ".travis.yml").is_file()
    assert (project_path / "appveyor.yml").is_file()


    assert project_path.is_dir()
    conanfile_path = project_path / "conanfile.py"
    assert conanfile_path.is_file()

    conan.inspect(str(conanfile_path), ("name", "version", ))
    return conanfile_path


def test_valid_template_type(valid_template_type, tmpdir, conan):
    """ Generate valid project """
    name = "conan-testname"
    outputpath = pathlib.Path(tmpdir.strpath)

    _test_valid_template_type(valid_template_type, outputpath, conan)


def test_invalid_template_type(tmpdir):
    """ Cannot generate project because invalid template type """
    name = "conan-testname"
    outputpath = pathlib.Path(tmpdir.strpath)
    invalid_template_type = "nonsense"
    try:
        generate_project(template_type=invalid_template_type, output=outputpath, name=name)
        assert False, "An error should have been thrown"
    except InvalidArgumentError:
        pass


def test_default_template(tmpdir, conan):
    outputpath = pathlib.Path(tmpdir.strpath)
    c = _test_valid_template_type("default", outputpath, conan)

    answer = conan.inspect(str(c), ("settings", "options", ))

    assert answer["settings"] is not None
    assert answer["options"] is not None

    assert "os" in answer["settings"]
    assert "arch" in answer["settings"]

    assert "os_build" not in answer["settings"]
    assert "arch_build" not in answer["settings"]

    assert "compiler" in answer["settings"]
    assert "build_type" in answer["settings"]
    assert "shared" in answer["options"]
    assert "fPIC" in answer["options"]


def test_header_only_template(tmpdir, conan):
    outputpath = pathlib.Path(tmpdir.strpath)
    c = _test_valid_template_type("header_only", outputpath, conan)

    answer = conan.inspect(str(c), ("settings", "options", ))

    assert answer["settings"] is None
    assert answer["options"] is None


def test_install_only_template(tmpdir, conan):
    outputpath = pathlib.Path(tmpdir.strpath)
    c = _test_valid_template_type("installer_only", outputpath, conan)

    answer = conan.inspect(str(c), ("settings", "options", ))

    assert answer["settings"] is not None
    assert answer["options"] is None

    assert "os" not in answer["settings"]
    assert "arch" not in answer["settings"]

    assert "os_build" in answer["settings"]
    assert "arch_build" in answer["settings"]


    # assert "compiler" in answer["settings"]
    assert "build_type" not in answer["settings"]


