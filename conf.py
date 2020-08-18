# Configuration file for the Sphinx documentation builder.

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath("."))


# -- Project information -----------------------------------------------------

project = "RBniCS Project"
copyright = "2015-, Francesco Ballarin (and contributors)"
author = "Francesco Ballarin (and contributors)"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named "sphinx.ext.*") or your custom
# ones.
extensions = [
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------
html_title = "RBniCS - reduced order modelling in FEniCS"

# The theme to use for HTML and HTML Help pages.
# From https://github.com/bashtage/sphinx-material
html_theme = "sphinx_material"

# Material theme options
html_theme_options = {
    # Set the name of the project to appear in the navigation.
    "nav_title": "RBniCS Project",

    # Set you GA account ID to enable tracking
    "google_analytics_account": "UA-66224794-4",

    # Specify a base_url used to generate sitemap.xml. If not
    # specified, then no sitemap will be built.
    "base_url": "https://www.rbnicsproject.org",

    # Set the color and the accent color
    "theme_color": "#065895",
    "color_primary": "mathlab",
    "color_accent": "mathlab",

    # Set the repo location to get a badge with stats
    "repo_url": "https://github.com/RBniCS/RBniCS/",
    "repo_name": "RBniCS",

    # Visible levels of the global TOC; -1 means unlimited
    "globaltoc_depth": 1,
    # If False, expand all TOC entries
    "globaltoc_collapse": True,
    # If True, show hidden TOC entries
    "globaltoc_includehidden": False,

    # Path to a touch icon, should be 152x152 or larger.
    "touch_icon": "images/rbnics-logo-small.png",
    "logo_icon": "&#xe069",

    # Main menu links
    "nav_links": [
        {
            "href": "tutorials",
            "internal": True,
            "title": "Tutorials",
        },
        {
            "href": "installing",
            "internal": True,
            "title": "Installation",
        },
        {
            "href": "contributing",
            "internal": True,
            "title": "How to contribute",
        },
        {
            "href": "citing",
            "internal": True,
            "title": "How to cite",
        },
        {
            "href": "publications",
            "internal": True,
            "title": "Publications",
        },
    ],
}
html_sidebars = {
    "**": ["logo-text.html", "globaltoc.html", "localtoc.html", "searchbox.html"]
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# Custom CSS files
html_css_files = [
    "css/custom.css",
]