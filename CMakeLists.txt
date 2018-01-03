project(cmake_wrapper)

include(conanbuildinfo.cmake)
conan_basic_setup()

include("source_subfolder")
