#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, tools
import os


class LibnameConan(ConanFile):
    name = "libname"
    version = "0.0.0"
    url = "https://github.com/bincrafters/conan-libname"
    description = "Keep it short"
    
    # Indicates License type of the packaged library
    license = "MIT"
    
    # Packages the license for the conanfile.py
    exports = ["LICENSE.md"]
    
    # Custom attributes for Bincrafters recipe conventions
    source_folder = "source_folder"
    
    def source(self):
        source_url = "https://github.com/libauthor/libname"
        tools.get("{0}/archive/v{1}.tar.gz".format(source_url, self.version))
        extracted_dir = self.name + "-" + self.version

        #Rename to "source_folder" is a convention to simplify later steps
        os.rename(extracted_dir, self.source_folder)


    def package(self):
        include_folder = os.path.join(self.source_folder, "include")
        self.copy(pattern="LICENSE")
        self.copy(pattern="*", dst="include", src=include_folder)

    def package_id(self):
        self.info.header_only()
