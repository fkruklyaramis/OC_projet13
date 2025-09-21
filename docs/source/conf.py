"""
Configuration Sphinx ultra-simple pour Read The Docs.
"""

# -- Informations du projet --
project = 'OC-Lettings-Site'
copyright = '2025, OpenClassrooms'
author = 'OpenClassrooms'
version = '1.0'
release = '1.0.0'

# -- Configuration générale --
extensions = []
templates_path = ['_templates']
exclude_patterns = []
language = 'fr'

# -- Options HTML --
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
