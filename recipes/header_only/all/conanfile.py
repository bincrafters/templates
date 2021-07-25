from conans import ConanFile, tools
import os

required_conan_version = ">=1.33.0"


class LibnameConan(ConanFile):
    name = "libname"
    description = "Keep it short"
    topics = ("libname", "logging")
    url = "https://github.com/bincrafters/community"
    homepage = "https://github.com/original_author/original_lib"
    license = "MIT"  # Indicates license type of the packaged library; please use SPDX Identifiers https://spdx.org/licenses/
    no_copy_source = True

    settings = "os", "arch", "compiler", "build_type"

    _source_subfolder = "source_subfolder"

    def package_id(self):
        self.info.header_only()

    def source(self):
        tools.get(**self.conan_data["sources"][self.version], strip_root=True, destination=self._source_subfolder)

    def package(self):
        include_folder = os.path.join(self._source_subfolder, "include")
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        self.copy(pattern="*", dst="include", src=include_folder)
