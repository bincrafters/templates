#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, tools
import os


class LibnameConan(ConanFile):
    name = "libname"
    version = "0.0.0"
    url = "https://github.com/bincrafters/conan-libname"
    description = "Keep it short"
    license = "https://github.com/someauthor/somelib/blob/master/LICENSES"
    exports_sources = ["CMakeLists.txt", "LICENSE"]
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    #use static org/channel for libs in conan-center
    #use version ranges for dependencies unless there's a reason not to
    requires = "OpenSSL/[>=1.0.2l]@conan/stable", \
        "zlib/[>=1.2.11]@conan/stable"
        
    def requirements(self):
        #use dynamic org/channel for libs in bincrafters
        self.requires.add("libuv/[>=1.15.0]@bincrafters/stable")

    def source(self):
        source_url = "https://github.com/libauthor/libname"
        tools.get("{0}/archive/v{1}.tar.gz".format(source_url, self.version))
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, "sources")
        #Rename to "sources" is a convention to simplify later steps

    def package(self):
        self.copy(pattern="LICENSE")
        self.copy(pattern="*", dst="include", src="include")

    def package_id(self):
        self.info.header_only()
