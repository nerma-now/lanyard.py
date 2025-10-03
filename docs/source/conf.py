import os
import sys

sys.path.insert(0, os.path.abspath('../../src'))

project = 'lanyard.py'
copyright = '2025, Nikita (nerma-now)'
author = 'Nikita (nerma-now)'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    'sphinx.ext.autosummary',
    'sphinx.ext.inheritance_diagram',
]

templates_path = ['_templates']
exclude_patterns = []

html_theme = 'alabaster'
html_baseurl = 'https://nerma-now.github.io/lanyard.py/'

html_theme_options = {
    'extra_nav_links': {
        'PyPI': 'https://pypi.org/project/lanyard-py/',
        'Github': 'https://github.com/nerma-now/lanyard.py',
    },
}

autoclass_content = 'both'

autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
}
autodoc_typehints = 'description'