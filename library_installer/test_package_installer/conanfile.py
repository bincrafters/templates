#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from conans import ConanFile, tools, CMake


class TestPackageConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch",
    generators = "cmake",

    def test(self):
        if not tools.cross_building(self.settings):
            self.run("some_executable", run_environment=True)
