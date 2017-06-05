import unittest

import logging

import pypluggy
import pylogconf

from pypluggy.mgr import Mgr

pylogconf.setup()


class TestNames(unittest.TestCase):
    def testList(self):
        m = Mgr()
        m.load_modules()
        self.assertListEqual(m.list_names(cls=unittest.TestCase, check_type=type), ['TestNames'], msg='uh uh')

    def testInstantiate(self):
        m = Mgr()
        m.load_modules()
        t = m.instantiate_name(cls=unittest.TestCase, name='TestNames')
        self.assertIsInstance(t, unittest.TestCase)
