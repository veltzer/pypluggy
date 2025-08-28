"""
This is a light weight plugin based system
"""

import pkgutil  # for iter_modules
import logging  # for getLogger
import os.path  # for isdir
import importlib  # for import_module
from typing import Any


class Mgr:
    def __init__(self, strict=True):
        self.module_names_loaded = set()
        self.modules_loaded = set()
        self.strict = strict
        self.classes_instantiated = {}

    def load_modules(self, folder=".", prefix=""):
        """
        :param folder:
        :param prefix:
        :return:

        example of input:
        folder="pipeline/plugins"
        prefix="pipeline.plugins."
        """
        logger = logging.getLogger(__name__)
        logger.debug("starting")
        assert os.path.isdir(folder)
        assert prefix is not None
        for _importer, modname, _ in pkgutil.walk_packages(path=[folder], prefix=prefix):
            if modname in self.module_names_loaded:
                continue
            logger.debug(f"trying {modname}")
            try:
                m = importlib.import_module(modname)
                self.modules_loaded.add(m)
            # pylint: disable=broad-except
            except Exception as e:
                logger.debug(f"got exception {e}")
                if self.strict:
                    raise e
            logger.debug("loaded <%s>", modname)
            self.module_names_loaded.add(modname)

    def print(self):
        print(self.module_names_loaded)

    def yield_modules(self):
        yield from self.modules_loaded

    def find_and_instantiate(self, cls=None, check_type=type):
        assert cls not in self.classes_instantiated
        assert cls is not None
        inst_set = set()
        logger = logging.getLogger(__name__)
        for current_module in self.modules_loaded:
            for name, t in current_module.__dict__.items():
                logger.debug("trying <%s>", name)
                if isinstance(t, check_type):
                    logger.debug("instantiating <%s>", t)
                    instance = t()
                    inst_set.add(instance)
        self.classes_instantiated[cls] = inst_set
        return inst_set

    def list_names(self, cls=None, check_type=None):
        assert cls is not None
        assert check_type is not None
        results = []
        logger = logging.getLogger(__name__)
        for current_module in self.modules_loaded:
            for name, t in current_module.__dict__.items():
                logger.debug(f"trying {name} {t.__class__.__name__} {type(t)}")
                # if type(t) is check_type and issubclass(t, cls):
                if isinstance(t, check_type):
                    logger.debug(f"appending {name}")
                    results.append(t.__name__)
        return results

    def list_by_attr(self, attribute_name: str | None = None, attribute_value: str | None = None) -> list[str]:
        assert attribute_name is not None
        assert attribute_value is not None
        results = []
        logger = logging.getLogger(__name__)
        for current_module in self.modules_loaded:
            for name, t in current_module.__dict__.items():
                logger.debug(f"trying {name} {t.__class__.__name__} {type(t)}")
                if hasattr(t, attribute_name) and getattr(t, attribute_name) == attribute_value:
                    logger.debug(f"appending {name}")
                    results.append(t.__name__)
        return results

    def instantiate_by_attr_name(
            self,
            attribute_name: str,
            attribute_value: str | None = None,
            class_name: str | None = None,
    ) -> Any:
        logger = logging.getLogger(__name__)
        for current_module in self.modules_loaded:
            for name, t in current_module.__dict__.items():
                logger.debug(f"trying {name} {t.__class__.__name__} {type(t)}")
                if hasattr(t, attribute_name) and getattr(t, attribute_name) == attribute_value:
                    if name == class_name:
                        return t()
        raise ValueError("not found")

    def instantiate_name(self, cls=None, name=None):
        assert cls is not None
        assert name is not None
        logger = logging.getLogger(__name__)
        for current_module in self.modules_loaded:
            for cur_name, t in current_module.__dict__.items():
                logger.debug(f"trying {cur_name} {cls}")
                # if type(t) is type and issubclass(t, cls):
                if isinstance(t, cls):
                    logger.debug(f"considering {cur_name}")
                    if t.__name__ == name:
                        return t()
        raise ValueError(f"did not find your name {name}")
