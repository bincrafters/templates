#!/usr/bin/env python

from bincrafters import build_template_header_only

if __name__ == "__main__":

    builder = build_template_header_only.get_builder()

    builder.run()
