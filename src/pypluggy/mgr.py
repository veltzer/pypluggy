"""
This is a light weight plugin based system
"""

import pkgutil  # for iter_modules
import logging  # for getLogger
import os.path  # for isdir
import importlib  # for import_module

logger = logging.getLogger(__name__)


class Mgr:
    def __init__(self, strict=True):
        self.module_names_loaded = set()
        self.modules_loaded = set()
        self.strict = strict
        self.classes_instantiated = dict()

    def load_modules(self, folder='.', prefix=''):
        """
        :param folder:
        :param prefix:
        :return:

        example of input:
        folder='pipeline/plugins'
        prefix='pipeline.plugins.'
        """
        logger.debug("starting")
        assert os.path.isdir(folder)
        assert prefix is not None
        for importer, modname, is_pkg in pkgutil.walk_packages(path=[folder], prefix=prefix):
            if modname in self.module_names_loaded:
                continue
            logger.debug("trying <%s>", modname)
            try:
                m = importlib.import_module(modname)
                self.modules_loaded.add(m)
            except Exception as e:
                logger.debug("got exception <%s>", e)
                if self.strict:
                    raise e
            logger.debug("loaded <%s>", modname)
            self.module_names_loaded.add(modname)

    def print(self):
        print(self.module_names_loaded)

    def yield_modules(self):
        for module in self.modules_loaded:
            yield module

    def find_and_instantiate(self, cls=None, check_type=type):
        assert cls not in self.classes_instantiated
        assert cls is not None
        inst_set = set()
        for module in self.modules_loaded:
            for name, t in module.__dict__.items():
                logger.debug("trying <%s>", name)
                if type(t) is check_type and issubclass(t, cls):
                    logger.debug("instantiating <%s>", t)
                    instance = t()
                    inst_set.add(instance)
        self.classes_instantiated[cls] = inst_set
        return inst_set

    def list_names(self, cls=None):
        assert cls is not None
        results = []
        for module in self.modules_loaded:
            for name, t in module.__dict__.items():
                if type(t) is type and issubclass(t, cls):
                    results.append(t.__name__)
        return results

    def instantiate_name(self, cls=None, name=None):
        assert cls is not None
        assert name is not None
        for module in self.modules_loaded:
            for name, t in module.__dict__.items():
                if type(t) is type and issubclass(t, cls):
                    if t.__name__ == name:
                        return t()
        raise ValueError("did not find your name {}".format(name))


