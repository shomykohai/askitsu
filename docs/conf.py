# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
import re

sys.path.insert(0, os.path.abspath(".."))


# -- Project information -----------------------------------------------------

project = "askitsu"
copyright = "2022, ShomyKohai"
author = "ShomyKohai"

# The full version, including alpha/beta/rc tags
with open(f"../askitsu/__init__.py") as f:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE
    ).group(1)
release = version

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_autodoc_typehints",
    "sphinx_design",
    "sphinx_copybutton",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

rst_prolog = """
.. |coro| replace:: This function is a coroutine.
"""

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "furo"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

html_domain_indices = False

html_favicon = "./images/favicon.ico"

pygments_style = "sphinx"
pygments_dark_style = "monokai"


def remove_module_docstring(app, what, name, obj, options, lines):
    if what == "module" and name in (
        "client",
        "character",
        "core",
        "anime",
        "error",
        "manga",
    ):
        del lines[:]


def setup(app):
    app.connect("autodoc-process-docstring", remove_module_docstring)
