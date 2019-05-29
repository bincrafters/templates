# -*- coding: utf-8 -*-
{% set build_system = cookiecutter.build_system.lower().strip() %}{%
set build_system_conan_class = {"cmake": "CMake", "autotools": "AutoToolsBuildEnvironment"}[build_system] %}{%
set is_cmake = build_system == "cmake" %}{%
set is_autotools = build_system == "autotools" %}{%
set is_shared = cookiecutter.shared.lower() == "y" %}
from conans import ConanFile, {{build_system_conan_class}}, tools
import os


class {{cookiecutter.name.title().replace(" ", "")}}Conan(ConanFile):
    name = "{{cookiecutter.name}}"
    version = "{{cookiecutter.version}}"
    description = "{{cookiecutter.description}}"
    topics = ({% for topic in cookiecutter.topics.split(",") %}"{{topic}}", {% endfor %})
    url = "{{cookiecutter.url}}"
    homepage = "{{cookiecutter.homepage}}"
    author = "{{cookiecutter.author}} <{{cookiecutter.email}}>"
    license = "{{cookiecutter.license}}"
    exports = ["LICENSE.md"]
{% if is_cmake %}
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"
{% endif %}
    settings = "os", "arch", "compiler", "build_type"
{% if is_shared %}
    options = {"shared": [True, False], "fPIC": [True, False], }
    default_options = {"shared": False, "fPIC": True, }
{% endif %}
    _source_subfolder = "source_subfolder"{% if is_cmake %}
    _build_subfolder = "build_subfolder"{%endif%}
{% if cookiecutter.requires.lower == "n" %}
    requires = ({% for require in cookiecutter.requires.split(",")%}
        "{{require}}",{%endfor%}
    )
{% endif %}
    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def source(self):
        source_url = "{{cookiecutter.source_url}}".format(url=self.url, version=self.version)
        sha256 = "{{cookiecutter.sha256}}"
        tools.get(source_url, sha256=sha256)

        extracted_dir = "{{cookiecutter.extracted_dir}}".format(name=self.name, version=self.version)
        os.rename(extracted_dir, self._source_subfolder)
{% if is_cmake %}
    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_TESTS"] = False  # example
        cmake.configure(build_folder=self._build_subfolder)
        return cmake
{% elif is_autotools %}
    def _configure_autotools(self):
        autotools = AutoToolsEnvironment(self)
        arguments = [{% if is_shared %}
            "--enable-shared" if self.options.shared else "--disable-shared",
            "--disable-static" if self.options.shared else "--enable-static",{%endif%}
        ]
        autotools.configure(configure_dir=os.path.join(self.source_folder, self._source_subfolder), args=arguments)
        return autotools
{% endif %}
    def build(self):{% if is_cmake %}
        cmake = self._configure_cmake()
        cmake.build()
{% elif is_autotools %}
        autotools = self._configure_autotools()
        autotools.make()
{% else %}
        self.run("make")  # add custom build scripts here
{% endif %}
    def package(self):{%if is_cmake %}
        with tools.chdir(os.path.join(self.build_folder, self._build_subfolder)):
            cmake = self._configure_cmake()
            cmake.install
{% elif is_autotools %}
        with tools.chdir(os.path.join(self.build_folder)):
            autotools = self._configure_autotools()
            autotools.install()
{% else %}
        self.rum("make install")  # add custom install scripts here
{%endif%}
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        # If the build system has a proper install method, the steps below may be redundant
        # If so, you can just remove the lines below
        include_folder = os.path.join(self._source_subfolder, "include")
        self.copy(pattern="*", dst="include", src=include_folder)
        self.copy(pattern="*.dll", dst="bin", keep_path=False)
        self.copy(pattern="*.lib", dst="lib", keep_path=False)
        self.copy(pattern="*.a", dst="lib", keep_path=False)
        self.copy(pattern="*.so*", dst="lib", keep_path=False)
        self.copy(pattern="*.dylib", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
