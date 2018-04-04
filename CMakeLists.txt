project(cmake_wrapper)
cmake_minimum_required(VERSION 2.8.11)

include(conanbuildinfo.cmake)
conan_basic_setup()

add_subdirectory("source_subfolder")
