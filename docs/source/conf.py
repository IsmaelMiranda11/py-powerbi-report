import pathlib
import sys
import os
# conf.py is inside docs/source. So, it should return two folders
sys.path.insert(0, os.path.abspath('../..'))

# root_path = pathlib.Path('.').resolve().as_posix()
# root_root_path = pathlib.Path('..').resolve().as_posix()
# parent_file_path = pathlib.Path(__file__).parents[2]
# # The project folder path
# project_folder = parent_file_path.resolve().as_posix() 
# Set the module folder. It is inside project folder.
# module_name = 'pypbireport'
# module_path = pathlib.Path(parent_file_path, module_name).resolve().as_posix()
# # Adding paths to sys path and allowed the import
# sys.path.insert(0, root_path)
# sys.path.insert(0, root_root_path)
# sys.path.insert(0, project_folder)
# sys.path.insert(0, module_path)



# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'pypbireport'
copyright = '2023, Ismael Miranda'
author = 'Ismael Miranda'
release = '0.2'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.napoleon',
    'sphinx.ext.autodoc',
    # 'myst_parser',
    # 'nbsphinx',
    "myst_nb",
    'sphinx_copybutton'
]

templates_path = ['_templates']
exclude_patterns = []
# toc_object_entries_show_parents = 'all'
source_suffix = {
    '.rst': 'restructuredtext',
    '.txt': 'markdown',
    # '.md': 'markdown',
    # '.ipynb': 'myst-nb',
    # 'myst': 'myst-nb'
}

# autodoc_typehints = 'both'
# autodoc_mock_imports = ["pypbireport"]

# nb_custom_formats = {
#     ".md": ["jupytext.reads", {"fmt": "mystnb"}],
# }

nb_execution_mode = 'off'
nb_number_source_lines = True



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_split_index = True
# html_sidebars = {
#    '**': ['globaltoc.html', 'sourcelink.html', 'searchbox.html'],
#    'using/windows': ['windowssidebar.html', 'searchbox.html'],
# }