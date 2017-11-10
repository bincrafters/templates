[ ![Download](https://api.bintray.com/packages/bincrafters/public-conan/somelib%3Abincrafters/images/download.svg) ](https://bintray.com/bincrafters/public-conan/somelib%3Abincrafters/_latestVersion)
[![Build Status](https://travis-ci.org/bincrafters/conan-somelib.svg?branch=stable%2F0.0.0)](https://travis-ci.org/bincrafters/conan-somelib)
[![Build status](https://ci.appveyor.com/api/projects/status/sxs9n6vb8nqa92l5?svg=true)](https://ci.appveyor.com/project/BinCrafters/conan-somelib)

[Conan.io](https://conan.io) package for [somelib](https://github.com/someauthor/somelib) project

The packages generated with this **conanfile** can be found in [Bintray](https://bintray.com/bincrafters/public-conan/somelib%3Abincrafters).

## For Users: Use this package

### Basic setup

    $ conan install somelib/0.0.0@bincrafters/stable

### Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*

    [requires]
    somelib/0.0.0@bincrafters/stable

    [generators]
    txt

Complete the installation of requirements for your project running:

    $ mkdir build && cd build && conan install ..

Note: It is recommended that you run conan install from a build directory and not the root of the project directory.  This is because conan generates *conanbuildinfo* files specific to a single build configuration which by default comes from an autodetected default profile located in ~/.conan/profiles/default .  If you pass different build configuration options to conan install, it will generate different *conanbuildinfo* files.  Thus, they should not be added to the root of the project, nor committed to git.

## For Packagers: Publish this Package

The example below shows the commands used to publish to bincrafters conan repository. To publish to your own conan respository (for example, after forking this git repository), you will need to change the commands below accordingly.

## Build and package

The following command both runs all the steps of the conan file, and publishes the package to the local system cache.  This includes downloading dependencies from "build_requires" and "requires" , and then running the build() method.

    $ conan create bincrafters/stable

## Add Remote

    $ conan remote add bincrafters "https://api.bintray.com/conan/bincrafters/public-conan"

## Upload

    $ conan upload somelib/0.0.0@bincrafters/stable --all -r bincrafters

## License
[LICENSE_TYPE](LICENSE)
