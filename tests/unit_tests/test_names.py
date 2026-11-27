"""
test_names.py
"""

import unittest

import pylogconf.core

from pypluggy.mgr import Mgr

pylogconf.core.setup()


class TestNames(unittest.TestCase):
    @unittest.skip("doesnt work")
    def test_list(self) -> None:
        m = Mgr()
        m.load_modules()
        assert m.list_names(cls=unittest.TestCase, check_type=type) == ["TestNames"], "uh uh"

    @unittest.skip("doesnt work")
    def test_instantiate(self) -> None:
        m = Mgr()
        m.load_modules()
        t = m.instantiate_name(cls=unittest.TestCase, name="TestNames")
        assert isinstance(t, unittest.TestCase)
