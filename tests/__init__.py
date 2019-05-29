# -*- coding: utf-8 -*-

from conans.client.conan_api import Conan
import pytest


@pytest.fixture(scope="session")
def conan():
    conan, _, _= Conan.factory(False)
    return conan
