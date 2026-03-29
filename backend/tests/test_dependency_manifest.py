from pathlib import Path


def test_httpx_declares_socks_support() -> None:
    pyproject = Path(__file__).resolve().parents[1] / "pyproject.toml"
    content = pyproject.read_text()

    assert '"httpx[socks]>=0.28.1"' in content
