#!/usr/bin/env python
# -*- coding: utf-8 -*-


from bincrafters import build_template_installer, build_shared
import os

if __name__ == "__main__":

    arch = os.environ["ARCH"]
    builder = build_template_installer.get_builder()
    builder.add({"os" : build_shared.get_os(), "arch_build" : arch, "arch": arch}, {}, {}, {})
    builder.run()
