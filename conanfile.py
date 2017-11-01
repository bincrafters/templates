#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, tools
import os

class LibnameConan(ConanFile):
    name = "libname"
    version = "0.0.0"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    url = "https://github.com/bincrafters/conan-libname"
    description = "Keep it short"
    license = "https://github.com/someauthor/somelib/blob/master/LICENSES"
    root = name + "-" + version
    #use static org/channel for libs in conan-center
    #use dynamic org/channel for libs in bincrafters
    requires = "OpenSSL/1.0.2l@conan/stable", \
        "zlib/1.2.11@conan/stable", \
        "websocketpp/0.7.0@%s/%s" % (self.user, self.channel)

    def source(self):
        source_url = "https://github.com/Microsoft/cpprestsdk"
        tools.get("{0}/archive/v{1}.tar.gz".format(source_url, self.version))

    def build(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_TESTS"] = False
        cmake.configure()
        cmake.build()

    def package(self):
        self.copy(pattern="*", dst="include", src="include")
        self.copy(pattern="*.dll", dst="bin", src="bin", keep_path=False)
        self.copy(pattern="*.lib", dst="lib", src="lib", keep_path=False)
        self.copy(pattern="*.a", dst="lib", src="lib", keep_path=False)
        self.copy(pattern="*.so*", dst="lib", src="lib", keep_path=False)
        self.copy(pattern="*.dylib", dst="lib", src="lib", keep_path=False)

    def package_info(self):
        tools.collect_libs(self)
