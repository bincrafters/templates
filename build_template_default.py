#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conan.packager import ConanMultiPackager
from conan import tools
import os
import re

def build():
    import template_filename  # pylint: disable=F0401
    build_bincrafters.build()
        
        
    name = get_name_from_recipe()
    username, channel, version = get_env_vars()
    reference = "{0}/{1}".format(name, version)
    upload = "https://api.bintray.com/conan/{0}/public-conan".format(username)

    builder = ConanMultiPackager(
        username=username,
        channel=channel,
        reference=reference,
        upload=upload,
        remotes=upload,  # while redundant, this moves bincrafters remote to position 0
        upload_only_when_stable=True,
        stable_branch_pattern="stable/*")

    builder.add_common_builds(shared_option_name=name + ":shared")
    builder.run()

    
