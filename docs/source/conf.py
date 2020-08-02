#import os
#import sys

#sys.path.insert(0, os.path.abspath('../..'))

#import sphinx_rtd_theme

project = 'docker-postgres-influxdb-grafana'
copyright = '2020, viktorsapozhok'
author = 'viktorsapozhok'
user = 'viktorsapozhok'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
]

# The suffix of source filenames.
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

language = "en"

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'sphinx_rtd_theme'

html_context = {
    'display_github': True,
    'github_user': user,
    'github_repo': project,
    'github_version': 'master',
    'conf_py_path': '/docs/source/',
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = []
