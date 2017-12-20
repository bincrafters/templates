#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class LibnameConan(ConanFile):
    name = "libname"
    version = "0.0.0"
    url = "https://github.com/bincrafters/conan-libname"
    description = "Keep it short"
    license = "https://github.com/someauthor/somelib/blob/master/LICENSES"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
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

    def build(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_TESTS"] = False # example
        cmake.configure(source_dir="sources")
        cmake.build()

    def package(self):
        with tools.chdir("sources"):
            self.copy("license*", dst="licenses",  ignore_case=True, keep_path=False)
            self.copy(pattern="*", dst="include", src="include")
            self.copy(pattern="*.dll", dst="bin", src="bin", keep_path=False)
            self.copy(pattern="*.lib", dst="lib", src="lib", keep_path=False)
            self.copy(pattern="*.a", dst="lib", src="lib", keep_path=False)
            self.copy(pattern="*.so*", dst="lib", src="lib", keep_path=False)
            self.copy(pattern="*.dylib", dst="lib", src="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
