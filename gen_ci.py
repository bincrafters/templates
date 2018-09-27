#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4


from __future__ import print_function
import argparse


def main():
    parser = argparse.ArgumentParser(description='gen_ci.py: generate .travis.yml and appveyor.yml files')
    parser.add_argument('--skip-appveyor', action='store_true',
                        help='skip appveyor.yml generation')
    parser.add_argument('--skip-travis', action='store_true',
                        help='skip .travis.yml generation')
    parser.add_argument('--gcc-versions', nargs='+',
                        help='generate builds only for specified GCC versions')
    parser.add_argument('--clang-versions', nargs='+',
                        help='generate builds only for specified Clang versions')
    parser.add_argument('--apple-clang-versions', nargs='+',
                        help='generate builds only for specified Apple Clang versions')
    parser.add_argument('--msvc-versions', nargs='+',
                        help='generate builds only for specified MSVC versions')
    parser.add_argument('--split-arch', action='store_true',
                        help='split builds by architecture')
    parser.add_argument('--split-build-type', action='store_true',
                        help='split builds by build type')
    parser.add_argument('--split-visual-runtime', action='store_true',
                        help='split builds by visual runtime')
    parser.add_argument('-p', '--pages', type=int,
                        help='split into additional conan pages')
    args = parser.parse_args()
    print(args)

    travis_template = """linux: &linux
   os: linux
   sudo: required
   language: python
   python: "3.6"
   services:
     - docker
osx: &osx
   os: osx
   language: generic
matrix:
   include:
{gcc_builds}
{clang_builds}
{apple_clang_builds}

install:
  - chmod +x .travis/install.sh
  - ./.travis/install.sh

script:
  - chmod +x .travis/run.sh
  - ./.travis/run.sh
"""

    appveyor_template = """build: false

environment:
    PYTHON: "C:\\\\Python27"
    PYTHON_VERSION: "2.7.15"
    PYTHON_ARCH: "32"

    matrix:
{mingw_builds}
{msvc_builds}

install:
  - set PATH=%PATH%;%PYTHON%/Scripts/
  - pip.exe install conan --upgrade
  - pip.exe install conan_package_tools bincrafters_package_tools
  - conan user # It creates the conan data directory

test_script:
  - python build.py
"""

    def format_msvc_build(version):
        appveyor_images = {'12': 'Visual Studio 2015',
                           '14': 'Visual Studio 2015',
                           '15': 'Visual Studio 2017'}

        msvc_template = """        - APPVEYOR_BUILD_WORKER_IMAGE: {image}
          CONAN_VISUAL_VERSIONS: {version}"""
        return msvc_template.format(image=appveyor_images[version],
                                    version=version)

    def format_gcc_build(version):
        gcc_template = """      - <<: *linux
        env: CONAN_GCC_VERSIONS={version} CONAN_DOCKER_IMAGE={image}"""
        image = 'lasote/conangcc%s' % version.replace('.', '')
        return gcc_template.format(image=image,
                                   version=version)

    def format_clang_build(version):
        clang_template = """      - <<: *linux
        env: CONAN_CLANG_VERSIONS={version} CONAN_DOCKER_IMAGE={image}"""
        image = 'lasote/conanclang%s' % version.replace('.', '')
        return clang_template.format(image=image,
                                     version=version)

    def format_apple_clang_build(version):
        xcode_images = {'7.3': 'xcode7.3',
                        '8.1': 'xcode8.3',
                        '9.0': 'xcode9',
                        '9.1': 'xcode9.4'
                        '10.0': 'xcode10'}
        apple_clang_template = """      - <<: *osx
        osx_image: {image}
        env: CONAN_APPLE_CLANG_VERSIONS={version}"""
        return apple_clang_template.format(image=xcode_images[version],
                                           version=version)

    def split_appveyor(builds, token, values):
        new_builds = []
        for b in builds:
            for value in values:
                # visual runtime is special case
                if token == 'CONAN_VISUAL_RUNTIME':
                    if 'CONAN_BUILD_TYPE: Debug' in b:
                        value += 'd'
                new_builds.append(b + '\n          {token}: {value}'.format(token=token, value=value))
        return new_builds

    def split_travis(builds, token, values):
        new_builds = []
        for b in builds:
            for value in values:
                new_builds.append(b + ' {token}={value}'.format(token=token, value=value))
        return new_builds

    def pages_appveyor(builds, pages):
        new_builds = []
        for b in builds:
            for n in range(0, pages):
                tail = '\n          CONAN_TOTAL_PAGES: %s\n          CONAN_CURRENT_PAGE: %s' % (pages, n)
                new_builds.append(b + tail)
        return new_builds

    def pages_travis(builds, pages):
        new_builds = []
        for b in builds:
            for n in range(0, pages):
                new_builds.append(b + ' CONAN_TOTAL_PAGES=%s CONAN_CURRENT_PAGE=%s' % (pages, n))
        return new_builds

    gcc_versions = args.gcc_versions or ['4.9', '5', '6', '7', '8']
    clang_versions = args.clang_versions or ['3.9', '4.0', '5.0', '6.0']
    apple_clang_versions = args.apple_clang_versions or ['7.3', '8.1', '9.0', '9.1']
    msvc_versions = args.msvc_versions or ['12', '14', '15']

    gcc_builds = [format_gcc_build(v) for v in gcc_versions]
    clang_builds = [format_clang_build(v) for v in clang_versions]
    apple_clang_builds = [format_apple_clang_build(v) for v in apple_clang_versions]
    # TODO : MinGW
    mingw_builds = [r"        #- MINGW_CONFIGURATIONS: "
                    r"'4.9@x86_64@seh@posix, "
                    r"4.9@x86_64@sjlj@posix, "
                    r"4.9@x86@sjlj@posix, "
                    r"4.9@x86@dwarf2@posix, "
                    r"6@x86_64@seh@posix, "
                    r"7@x86_64@seh@posix'"]
    msvc_builds = [format_msvc_build(v) for v in msvc_versions]

    # always split appveyor by build type
    msvc_builds = split_appveyor(msvc_builds, 'CONAN_BUILD_TYPES', ['Release', 'Debug'])

    if args.split_build_type:
        gcc_builds = split_travis(gcc_builds, 'CONAN_BUILD_TYPES', ['Release', 'Debug'])
        clang_builds = split_travis(clang_builds, 'CONAN_BUILD_TYPES', ['Release', 'Debug'])
        apple_clang_builds = split_travis(apple_clang_builds, 'CONAN_BUILD_TYPES', ['Release', 'Debug'])

    if args.split_arch:
        msvc_builds = split_appveyor(msvc_builds, 'CONAN_ARCHS', ['x86', 'x86_64'])
        gcc_builds = split_travis(gcc_builds, 'CONAN_ARCHS', ['x86', 'x86_64'])
        clang_builds = split_travis(clang_builds, 'CONAN_ARCHS', ['x86', 'x86_64'])
        # NOTE : Apple Clang is intentionally omitted, as we build only x86_64 for OSX

    if args.split_visual_runtime:
        msvc_builds = split_appveyor(msvc_builds, 'CONAN_VISUAL_RUNTIME', ['MT', 'MD'])

    if args.pages:
        msvc_builds = pages_appveyor(msvc_builds, args.pages)
        gcc_builds = pages_travis(gcc_builds, args.pages)
        clang_builds = pages_travis(clang_builds, args.pages)
        apple_clang_builds = pages_travis(apple_clang_builds, args.pages)

    gcc_builds = '\n'.join(gcc_builds)
    clang_builds = '\n'.join(clang_builds)
    apple_clang_builds = '\n'.join(apple_clang_builds)
    mingw_builds = '\n'.join(mingw_builds)
    msvc_builds = '\n'.join(msvc_builds)

    if not args.skip_travis:
        print('generating .travis.yml ...')
        with open('.travis.yml', 'w') as f:
            f.write(travis_template.format(gcc_builds=gcc_builds,
                                           clang_builds=clang_builds,
                                           apple_clang_builds=apple_clang_builds))
        print('generating .travis.yml ... DONE!')
    else:
        print('skipping .travis.yml generation')

    if not args.skip_appveyor:
        print('generating appveyor.yml...')
        with open('appveyor.yml', 'w') as f:
            f.write(appveyor_template.format(mingw_builds=mingw_builds,
                                             msvc_builds=msvc_builds))
        print('generating appveyor.yml... DONE!')
    else:
        print('skipping appveyor.yml generation')


if __name__ == '__main__':
    main()
