#!/usr/bin/env python

from bincrafters import build_template_default, build_template_installer, build_shared
import os

if __name__ == "__main__":
    if "CONAN_CONANFILE" in os.environ and os.environ["CONAN_CONANFILE"] == "conanfile_installer.py":
        arch = os.environ["ARCH"]
        builder = build_template_installer.get_builder()
        settings = {"os": build_shared.get_os(), "arch_build": arch, "arch": arch}

        builder.add(settings, {}, {}, {})
        builder.run()
    else:
        builder = build_template_default.get_builder(pure_c=True)
        builder.run()
