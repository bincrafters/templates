#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conan.packager import ConanMultiPackager
import os
import re
import platform


def get_value_from_recipe(search_string):
    with open("conanfile.py", "r") as conanfile:
        contents = conanfile.read()
        result = re.search(search_string, contents)
    return result


def get_name_from_recipe():
    return get_value_from_recipe(r'''name\s*=\s*["'](\S*)["']''').groups()[0]

    
def get_version_from_recipe():
    return get_value_from_recipe(r'''version\s*=\s*["'](\S*)["']''').groups()[0]

    
def get_ci_vars():
    reponame_a = os.getenv("APPVEYOR_REPO_NAME","")
    repobranch_a = os.getenv("APPVEYOR_REPO_BRANCH","")

    reponame_t = os.getenv("TRAVIS_REPO_SLUG","")
    repobranch_t = os.getenv("TRAVIS_BRANCH","")

    username, _ = reponame_a.split("/") if reponame_a else reponame_t.split("/")
    channel, version = repobranch_a.split("/") if repobranch_a else repobranch_t.split("/")
    return username, channel, version

    
def get_username_from_ci(): 
    username, _, _ = get_ci_vars()
    return username
   
   
def get_channel_from_ci(): 
    _, channel, _ = get_ci_vars()
    return channel
   
   
def get_version_from_ci(): 
    _, _, version = get_ci_vars()
    return version
    

def get_version():
    ci_ver = get_version_from_ci()
    recipe_ver = get_version_from_recipe()
    return ci_ver if ci_ver else recipe_ver
    
    
def get_env_vars():
    username = os.getenv("CONAN_USERNAME", get_username())
    channel = os.getenv("CONAN_CHANNEL", get_channel())
    version = os.getenv("CONAN_VERSION", get_version())
    return username, channel, version


def get_os():
    return platform.system().replace("Darwin", "Macos")

