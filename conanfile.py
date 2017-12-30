#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
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
    
    # Remove following lines if the target lib does not use cmake.
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake" 
    
    # Options may need to change depending on the packaged library. 
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    
    # Custom attributes for Bincrafters recipe conventions
    source_folder = "source_folder"
    build_folder = "build_folder"
    
    # Use version ranges for dependencies unless there's a reason not to
    requires = (
        "OpenSSL/[>=1.0.2l]@conan/stable",
        "zlib/[>=1.2.11]@conan/stable"
    )
        
    def source(self):
        source_url = "https://github.com/libauthor/libname"
        tools.get("{0}/archive/v{1}.tar.gz".format(source_url, self.version))
        extracted_dir = self.name + "-" + self.version

        #Rename to "source_folder" is a convention to simplify later steps
        os.rename(extracted_dir, self.source_folder)

        # Helper method for common CMake configurations
        wrap_cmake()

        
    def build(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_TESTS"] = False # example
        cmake.configure(source_folder=self.source_folder, build_folder=self.build_folder)
        cmake.build()
        cmake.install()
        
    def package(self):
        # If the CMakeLists.txt has a proper install method, the steps below may be redundant
        # If so, you can replace all the steps below with the word "pass"
        include_folder = os.path.join(self.source_folder, "include")
        self.copy(pattern="LICENSE")
        self.copy(pattern="*", dst="include", src=include_folder)
        self.copy(pattern="*.dll", dst="bin", keep_path=False)
        self.copy(pattern="*.lib", dst="lib", keep_path=False)
        self.copy(pattern="*.a", dst="lib", keep_path=False)
        self.copy(pattern="*.so*", dst="lib", keep_path=False)
        self.copy(pattern="*.dylib", dst="lib", keep_path=False)

        
    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

        
    # Helper method for common CMake configurations
    def wrap_cmake(self):
        with tools.chdir(self.source_folder):
            os.rename("CMakeLists.txt", "CMakeListsOriginal.txt")
        
        cmake_wrapper_new = os.path.join(self.source_folder, "CMakeLists.txt")
        os.rename("CMakeLists.txt", cmake_wrapper_new)
