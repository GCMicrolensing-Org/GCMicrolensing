"""
Sphinx configuration for the GCMicrolensing documentation.

This file configures the Sphinx documentation builder for the GCMicrolensing project.
"""

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

sys.path.insert(0, os.path.abspath(".."))

# -- Project information -----------------------------------------------------

project = "GCMicrolensing"
copyright = "2024, Gregory Costa Cuautle"
author = "Gregory Costa Cuautle"

# The full version, including alpha/beta/rc tags
release = "0.1.0"

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx.ext.mathjax",
    "nbsphinx",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "**.ipynb_checkpoints"]

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# -- Extension configuration -------------------------------------------------

# Autodoc configuration
autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "special-members": "__init__",
    "undoc-members": True,
    "exclude-members": "__weakref__",
}

# Napoleon configuration
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = True

# Intersphinx configuration
intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "matplotlib": ("https://matplotlib.org/stable/", None),
    "scipy": ("https://docs.scipy.org/doc/scipy/", None),
    "astropy": ("https://docs.astropy.org/en/stable/", None),
}

# NBSphinx configuration
nbsphinx_execute = "never"  # Don't execute notebooks on RTD


# Custom extension to generate animation GIF
def generate_animation_gif(app):
    """Generate the microlensing animation GIF during build."""
    import os
    import subprocess
    import sys

    try:
        # Get the docs directory
        docs_dir = os.path.dirname(__file__)
        script_path = os.path.join(docs_dir, "generate_animation.py")

        # Add the project root to Python path
        project_root = os.path.abspath(os.path.join(docs_dir, ".."))
        env = os.environ.copy()
        env["PYTHONPATH"] = f"{project_root}:{env.get('PYTHONPATH', '')}"

        print(f"Running animation generation script: {script_path}")
        result = subprocess.run(
            [sys.executable, script_path], cwd=docs_dir, env=env, capture_output=True, text=True
        )

        if result.returncode == 0:
            print("Animation GIF generated successfully!")
            if result.stdout:
                print(result.stdout)
        else:
            print(f"Warning: Animation generation failed: {result.stderr}")

    except Exception as e:
        print(f"Warning: Could not generate animation GIF: {e}")


def setup(app):
    """Configure Sphinx extension for automatic GIF generation."""
    app.connect("builder-inited", generate_animation_gif)


# -- Theme configuration -----------------------------------------------------

html_theme_options = {
    "navigation_depth": 4,
    "titles_only": False,
}
