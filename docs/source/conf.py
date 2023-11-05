import pathlib
import sys
# conf.py is inside docs/source. So, it should return two folders
parent_file_path = pathlib.Path(__file__).parents[2]
# The project folder path
project_folder = parent_file_path.resolve().as_posix() 
# Set the module folder. It is inside project folder.
module_name = 'pypbireport'
module_path = pathlib.Path(parent_file_path, module_name).resolve().as_posix()
# Adding paths to sys path and allowed the import
sys.path.insert(0, module_path)
sys.path.insert(0, project_folder)

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'pypbireport'
copyright = '2023, Ismael Miranda'
author = 'Ismael Miranda'
release = '0.3'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.napoleon',
    'sphinx.ext.autodoc'
]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
