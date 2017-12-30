#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conan.packager import ConanMultiPackager
from conans import tools
import importlib
import os


def get_module_location():
    repo = os.getenv("CONAN_MODULE_REPO", "https://raw.githubusercontent.com/bincrafters/conan-templates")
    branch = os.getenv("CONAN_MODULE_BRANCH", "package_tools_modules")
    return repo + "/" + branch

    
def get_module_name():
    return os.getenv("CONAN_MODULE_NAME", "build_template_default")

    
def get_module_filename():
    return get_module_name() + ".py"
    
    
def get_module_url():
    return get_module_location() + "/" + get_module_filename()

    
if __name__ == "__main__":
    
    tools.download(get_module_url(), get_module_filename(), overwrite=True)
    
    module = importlib.import_module(get_module_name())
    
    builder = module.get_builder()
    
    builder.run()

    