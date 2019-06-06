# -*- coding: utf-8 -*-

import os
from conanfile_base import ConanFileBase


class ConanInstaller(ConanFileBase):
    name = ConanFileBase._base_name + "_installer"
    version = ConanFileBase.version
    exports = ConanFileBase.exports + ["conanfile_base.py"]

    settings = "os_build", "arch_build", "compiler", "arch"

    def package_id(self):
        del self.info.settings.compiler
        del self.info.settings.arch

    def package_info(self):
        bindir = os.path.join(self.package_folder, "bin")
        self.output.info('Appending PATH environment variable: {}'.format(bindir))
        self.env_info.PATH.append(bindir)
