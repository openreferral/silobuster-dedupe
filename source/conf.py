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

# from inspect import getsourcefile
# from os.path import abspath

# # Make sure we are getting the absolute path to the training file!
# path_arr = abspath(getsourcefile(lambda:0)).split('/')
# path_arr.pop()
# curpath = '/'.join(path_arr)

# # sys.path.insert(0, curpath)
# # sys.path.insert(0, curpath + "/libs/")
# # sys.path.insert(0, curpath + "/libs/base_classes/")
sys.path.append('.')
sys.path.append('./libs')
sys.path.append('./libs/base_classes')
sys.path.append('./libs/connector')
sys.path.append('./libs/handler')
sys.path.append('./libs/dataframes')
sys.path.append('./libs/log_handler')
sys.path.append('./libs/silobuster_exceptions')
# sys.path.append('./deduper')

# -- Project information -----------------------------------------------------

project = 'Silobuster Dedupe'
copyright = '2023, Silobuster Dedupe'
author = 'Jamey Harris'

# The full version, including alpha/beta/rc tags
release = '1.0.0'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'python_docs_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
