# Neuron Discovery

[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3106/)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![Code Coverage](https://codecov.io/gh/a-t-0/snn/branch/main/graph/badge.svg)](https://codecov.io/gh/a-t-0/neurondiscovery)

Finds neurons of a specific type using a grid search. You specify which
behaviour you want.

## Run

```bash
python -m src.neurondiscovery
```

### Updating

Build the pip package with:

```bash
pip install --upgrade pip setuptools wheel
pip install twine
```

Install the pip package locally with:

```bash
rm -r dist
rm -r build
python3 setup.py sdist bdist_wheel
pip install -e .
```

Upload the pip package to the world with:

```bash
rm -r dist
rm -r build
python3 setup.py sdist bdist_wheel
python3 -m twine upload dist/\*
```
