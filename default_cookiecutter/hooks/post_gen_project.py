#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
import subprocess


rootdir = os.path.dirname(os.path.realpath("{{ cookiecutter._template }}"))
print("rootdir is", rootdir)


def remove_main_cmakelists():
    os.remove("CMakeLists.txt")


def remove_travis():
    os.remove(".travis.yml")


def copy_ci_scripts():
    ci_path = os.path.join(rootdir, ".ci")
    shutil.copytree(ci_path, ".ci")


def remove_appveyor():
    os.remove("appveyor.yml")


def main():
    is_cmake = "{{ cookiecutter.build_system }}".lower().strip() == "cmake"

    if not is_cmake:
        remove_main_cmakelists()

    travis_linux = "{{ cookiecutter.travis_linux }}".lower().strip() == "y"
    travis_macos = "{{ cookiecutter.travis_macos }}".lower().strip() == "y"
    appveyor_msvc = "{{ cookiecutter.appveyor_msvc }}".lower().strip() == "y"
    appveyor_mingw = "{{ cookiecutter.appveyor_mingw }}".lower().strip() == "y"

    if travis_linux or travis_macos:
        copy_ci_scripts()
    else:
        remove_travis()

    if not appveyor_msvc and not appveyor_mingw:
        remove_appveyor()

    is_git = "{{ cookiecutter.git }}".lower().strip() == "y"

    if is_git:
        subprocess.check_call(["git", "init"])
        subprocess.check_call(["git", "checkout", "-b", "testing/{{ cookiecutter.version }}",])
        subprocess.check_call(["git", "commit", "--allow-empty", "-m", "Initial commit"])
        subprocess.check_call(["git", "remote", "add", "origin", "{{cookiecutter.git_origin}}"])

        subprocess.check_call(["conan-readme-generator"])


if __name__ == "__main__":
    main()
