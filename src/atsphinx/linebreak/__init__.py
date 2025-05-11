"""Enable line-break for everywhere.."""

from docutils import nodes
from sphinx.application import Sphinx

__version__ = "0.1.3"


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
        # Check if the parent of the text node is a literal_block.
        # If so, skip processing to preserve code block structure.
        if isinstance(text.parent, nodes.literal_block):
            continue

        # NOTE: This may not catch CR+LF (windows) pattern.
        # Consider using text.astext().splitlines() for robust line splitting.
        if "\n" not in text.astext():  # Use astext() for reliable newline check
            continue

        # It's generally safer to work with copies or build a new list of nodes
        # rather than modifying the list while iterating or indexing into it.
        current_parent = text.parent
        if not current_parent:
            continue

        original_text_content = text.astext()
        lines = original_text_content.split("\n")

        # Only proceed if there are actual line breaks resulting in multiple lines
        if len(lines) <= 1 and not original_text_content.endswith("\n"):
            continue

        new_nodes = []
        for i, line_content in enumerate(lines):
            if line_content:  # Add text node only if there is content
                new_nodes.append(nodes.Text(line_content))

            # Add line_break node after each line except the last one,
            # or if the original text ended with a newline.
            if i == len(lines) - 1:
                if len(lines) == 1 or not original_text_content.endswith("\n"):
                    continue
            # Ensure not to add <br> if it's the very last empty string from a trailing newline
            # unless there was content before it.
            if line_content or i < len(lines) - 1:
                new_nodes.append(line_break())

        if not new_nodes:
            continue

        # Replace the original text node with the new sequence of text and line_break nodes
        text_pos = current_parent.index(text)
        current_parent.pop(text_pos)
        for i, new_node in enumerate(new_nodes):
            current_parent.insert(text_pos + i, new_node)


def setup(app: Sphinx):  # noqa: D103
    app.connect("doctree-read", inject_line_break)
    app.add_node(line_break, html=(visit_line_break, depart_line_break))
    return {
        "version": __version__,
        "env_version": 1,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
