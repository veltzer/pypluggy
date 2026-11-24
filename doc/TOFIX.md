# TOFIX

Findings from a code scan on 2026-10-04.

## High

- `src/pypluggy/mgr.py:118` - `instantiate_name` tests `isinstance(t, cls)`, but plugins are classes, and a class object is never an instance of the base class it subclasses, so this never matches and always raises `ValueError`. Use `isinstance(t, type) and issubclass(t, cls)` (the intended check is still visible in the commented line 117).
- `src/pypluggy/mgr.py:62` - `find_and_instantiate` never uses `cls` for filtering: with the default `check_type=type` it instantiates every class found in every loaded module, including imported ones (e.g. anything a plugin imports at module level). Filter with `issubclass(t, cls)` and skip `cls` itself. `list_names` (line 78) has the same bug (its `issubclass` check is commented out on line 77).
- `tests/unit_tests/test_names.py:12` - both tests are `@unittest.skip("doesnt work")` (lines 12 and 18), so the package has no running tests and the bugs above go unnoticed. Rewrite them against a small fixture plugin package (e.g. `tests/fixtures/plugins/`) passed to `load_modules(folder=..., prefix=...)`, instead of the default `folder="."`, and remove the skips.

## Medium

- `src/pypluggy/mgr.py:45` - in non-strict mode a module that failed to import still logs "loaded" and is added to `module_names_loaded` (line 46), so the failure is hidden and the module is never retried. Log the failure at warning level and only record successfully imported modules.
- `src/pypluggy/mgr.py:31` - argument validation is done with `assert` (also lines 32, 55-56, 70-71, 84-85, 111-112), which disappears under `python -O`. Raise `ValueError`/`TypeError` instead, and make the required parameters non-optional instead of `=None` plus an assert.
- `pyproject.toml:34` - runtime dependency `pytconf` is never imported anywhere in `src/` or `tests/`; remove it (and refresh `uv.lock`).
- `rsconstruct.toml:27` - `[processor.ruff]` and `[processor.mypy]` (line 31) list `config` in `src_dirs`, but `config/` holds only `.lua` files. List only `src` and `tests`.
- `README.md:6` - the generated README has no usage information for the library. Add a `tera.snippets/main.md.tera` (the include hook already in `tera.templates/README.md.tera:40`) showing `Mgr().load_modules(...)` and `find_and_instantiate`.

## Low

- `src/pypluggy/mgr.py:40` - stale `# pylint: disable=broad-except` comment; pylint is no longer used (ruff is).
- `src/pypluggy/mgr.py:12` - class `Mgr` and most public methods have no docstrings or type hints, while `sphinx/pypluggy.rst` publishes them with `:undoc-members:`.
- `doc/TODO.txt:1` - empty file; delete it.
- `pyproject.toml:83` - `mypy_path = "src:python:scripts"` names `python` and `scripts`, which do not exist here (the same line is in other py* repos such as pytimer, so fix it fleet-wide).
