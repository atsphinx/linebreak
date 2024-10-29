"""Standard tests."""

import pytest
from bs4 import BeautifulSoup
from sphinx.testing.util import SphinxTestApp


@pytest.mark.sphinx("html")
def test__it(app: SphinxTestApp):
    """Test to pass."""
    app.build()
    soup = BeautifulSoup((app.outdir / "index.html").read_text(), "lxml")
    assert soup.p.br
    soup = BeautifulSoup((app.outdir / "index2.html").read_text(), "lxml")
    assert soup.p.br
