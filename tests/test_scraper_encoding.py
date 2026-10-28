"""kanji_extractor.scraper のエンコーディング処理テスト。"""

from unittest.mock import MagicMock, patch

from kanji_extractor.scraper import _fetch_with_beautifulsoup


def test_fetch_with_beautifulsoup_apparent_encoding_fallback() -> None:
    mock_resp = MagicMock()
    mock_resp.encoding = "ISO-8859-1"
    mock_resp.apparent_encoding = "utf-8"
    mock_resp.content = "<html><body><p>日本語テスト</p></body></html>".encode()
    mock_resp.raise_for_status.return_value = None

    with patch("requests.get", return_value=mock_resp):
        text = _fetch_with_beautifulsoup("https://example.com/news")
        assert "日本語テスト" in text
