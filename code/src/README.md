# Shared source package

The checkout-local application package lives at
[`docxology_tools/__init__.py`](docxology_tools/__init__.py). Shared modules remain
in this directory; runnable command entry points remain in
[`code/orchestrators/`](../orchestrators/).

Import shared modules through `docxology_tools.<module>`. The bootstrap provides
the compatibility paths required by existing orchestrators and makes flat and
canonical imports refer to the same module object. Class identity, exception
catching and module state therefore survive either import order. Package import
is lazy and does not load optional browser or PDF libraries.

The explicit module registry covers every shared Python source. Its
[regressions](../tests/test_package_namespace.py) check registry completeness,
real modules in both import orders, and exception catching in a minimal
checkout. Add a new shared module to that registry rather than introducing
another path bootstrap or import alias.

This repository is an application with surrounding source data, not an
installable wheel. [`pyproject.toml`](../../pyproject.toml) declares that boundary.
Run its supported maintenance commands from the checkout, starting with
`uv run python3 code/orchestrators/agent.py status --json`. The
[development guide](../../docs/operations/development.md) defines environment,
generation, verification and landing contracts.
