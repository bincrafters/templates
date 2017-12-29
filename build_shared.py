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


def is_ci_running():
    return os.getenv("APPVEYOR_REPO_NAME", "") or os.getenv("TRAVIS_REPO_SLUG", "")


def get_repo_name_from_ci():
    reponame_a = os.getenv("APPVEYOR_REPO_NAME","")
    reponame_t = os.getenv("TRAVIS_REPO_SLUG","")
    return reponame_a if reponame_a else reponame_t

    
def get_repo_branch_from_ci():
    repobranch_a = os.getenv("APPVEYOR_REPO_BRANCH","")
    repobranch_t = os.getenv("TRAVIS_BRANCH","")
    return repobranch_a if repobranch_a else repobranch_t

    
def get_ci_vars():
    reponame = get_repo_name_from_ci()
    reponame_split = reponame.split("/")
    
    repobranch = get_repo_branch_from_ci()
    repobranch_split = repobranch.split("/")
    
    username, _ = reponame_split if len(reponame_split) > 1 else ["",""]
    channel, version = repobranch_split if len(repobranch_split) > 1 else ["",""]
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
    
    
def get_conan_vars():
    username = os.getenv("CONAN_USERNAME", get_username_from_ci())
    channel = os.getenv("CONAN_CHANNEL", get_channel_from_ci())
    version = os.getenv("CONAN_VERSION", get_version())
    return username, channel, version


def get_os():
    return platform.system().replace("Darwin", "Macos")
    

def get_builder():
    name = get_name_from_recipe()
    username, channel, version = get_conan_vars()
    reference = "{0}/{1}".format(name, version)
    upload = "https://api.bintray.com/conan/{0}/public-conan".format(username)
    remotes = os.getenv("CONAN_REMOTES", upload)
    upload_when_stable = os.getenv("CONAN_UPLOAD_ONLY_WHEN_STABLE", 1)
    stable_branch_pattern = os.getenv("CONAN_UPLOAD_ONLY_WHEN_STABLE", "stable/*")

    builder = ConanMultiPackager(
        username=username,
        channel=channel,
        reference=reference,
        upload=upload,
        remotes=remotes,  
        upload_only_when_stable=upload_when_stable,
        stable_branch_pattern=stable_branch_pattern)

    return builder
