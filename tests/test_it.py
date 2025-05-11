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
    assert soup.p.text == "This isa pen."
    assert len(soup.p.find_all("br")) == 1
    soup = BeautifulSoup((app.outdir / "index2.html").read_text(), "lxml")
    assert soup.p.br
    assert soup.p.text == "This isa pen."
    assert len(soup.p.find_all("br")) == 1


@pytest.mark.sphinx("html")
def test__code(app: SphinxTestApp):
    """Test for code-block with highlighting."""
    app.build()
    soup = BeautifulSoup((app.outdir / "code.html").read_text(), "lxml")
    _classes = soup.find("pre").parent.parent.get("class", [])  # got: 'body'
    assert "highlight-python" in _classes
