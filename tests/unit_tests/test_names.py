import unittest

import pylogconf.core

from pypluggy.mgr import Mgr

pylogconf.core.setup()


class TestNames(unittest.TestCase):
    @unittest.skip("doesnt work")
    def testList(self):
        m = Mgr()
        m.load_modules()
        self.assertListEqual(m.list_names(cls=unittest.TestCase, check_type=type), ['TestNames'], msg='uh uh')

    @unittest.skip("doesnt work")
    def testInstantiate(self):
        m = Mgr()
        m.load_modules()
        t = m.instantiate_name(cls=unittest.TestCase, name='TestNames')
        self.assertIsInstance(t, unittest.TestCase)
