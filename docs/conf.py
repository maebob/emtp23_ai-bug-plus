# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os 
import sys
from dotenv import load_dotenv


# load the .env file
load_dotenv()
# append the absolute_project_path from .env variable to the sys.path
sys.path.append(os.environ.get('absolute_project_path'))

sys.path.insert(0, os.path.abspath('../'))
project = 'BugPlus'
copyright = '2023, Aaron Steiner, Mae Turner and Mayte Dächer'
author = 'Aaron Steiner, Mae Turner and Mayte Dächer'
release = '0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx.ext.viewcode", "sphinx.ext.todo", "sphinx.ext.autodoc"]

templates_path = ['_templates']
html_theme = ['sphinx_rtd_theme']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

language = 'python'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
