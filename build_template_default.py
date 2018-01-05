#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conan.packager import ConanMultiPackager
from conans import tools
import importlib
import os
import re

def get_module_location():
    repo = os.getenv("CONAN_MODULE_REPO", "https://raw.githubusercontent.com/bincrafters/conan-templates")
    branch = os.getenv("CONAN_MODULE_BRANCH", "package_tools_modules")
    return repo + "/" + branch
    
def get_module_name():
    return "build_shared"

def get_module_filename():
    return get_module_name() + ".py"
    
def get_module_url():
    return get_module_location() + "/" + get_module_filename()
    
def get_builder(args=None):

    tools.download(get_module_url(), get_module_filename(), overwrite=True)

    module = importlib.import_module(get_module_name())
    
    package_name = module.get_name_from_recipe()
    
    builder = module.get_builder(args)

    builder.add_common_builds()
    
    return builder
    
