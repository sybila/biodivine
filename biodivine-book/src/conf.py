"""Sphinx configuration for the Biodivine book.

Build with ``make book`` from the book's directory, or by hand::

    .venv/bin/python -m sphinx -b html src _build

The book is written in MyST (Markdown), uses the Shibuya theme, and uses `sphinx-design` for the
language switch: every example is a tab set with a Rust and a Python tab that share sync groups, so
choosing a language switches every example on the page.
"""

project = "Biodivine"
copyright = "2026, Sybila"
author = "Sybila"

extensions = [
    "myst_parser",
    "sphinx_design",
    "sphinx.ext.intersphinx",
]

myst_enable_extensions = ["colon_fence", "deflist", "attrs_inline"]
# Heading anchors, so that cross-chapter links like `namespaces.md#no-magic` resolve.
myst_heading_anchors = 3
source_suffix = {".md": "markdown"}
master_doc = "index"

html_theme = "shibuya"
html_title = "The Biodivine book"
# Shibuya's options: https://shibuya.lepture.com/. The accent colour and the automatic colour mode
# are presentation choices; the AI/ads links the theme can add are switched off, because a library
# book should not advertise third-party services.
html_theme_options = {
    "accent_color": "violet",
    "color_mode": "auto",
    "show_ai_links": False,
    "github_url": "https://github.com/sybila/biodivine",
    "nav_links": [
        {"title": "XML DOM", "url": "xml-dom/index.html"},
    ],
}
exclude_patterns = ["_build"]
