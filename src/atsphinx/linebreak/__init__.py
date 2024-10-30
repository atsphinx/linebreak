"""Enable line-break for everywhere.."""

from docutils import nodes
from sphinx.application import Sphinx

__version__ = "0.0.0"


class line_break(nodes.Element, nodes.General):  # noqa: D101
    pass


def visit_line_break(self, node: line_break):
    """Inject br tag (html only)."""
    # NOTE: It can change inserting token by configuration.
    self.body.append("<br>")


def depart_line_break(self, node: line_break):
    """Do nothing."""
    pass


def inject_line_break(app: Sphinx, doctree: nodes.document):
    """Split text by line-break and inject marker node."""
    # NOTE: doctree["source"] has file path of source.
    # If it want to change proc by file type, see this.
    for text in doctree.findall(nodes.Text):
        # NOTE: This may not catch CR+LF (windows) pattern.
        if "\n" not in text:
            continue
        splitted = [(nodes.Text(t), line_break()) for t in text.split("\n")]
        items = [item for parts in splitted for item in parts]
        p = text.parent
        p.children = items[:-1]


def setup(app: Sphinx):  # noqa: D103
    app.connect("doctree-read", inject_line_break)
    app.add_node(line_break, html=(visit_line_break, depart_line_break))
    return {
        "version": __version__,
        "env_version": 1,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
