"""URLからニュース記事本文を取得するモジュール。

newspaper3k による抽出を優先し、本文が取得できなかった場合は
requests + BeautifulSoup による汎用的な本文抽出にフォールバックする。
"""

from __future__ import annotations

import logging

import requests
from bs4 import BeautifulSoup
from newspaper import Article

logger = logging.getLogger(__name__)

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)
REQUEST_TIMEOUT = 10  # 秒


class ArticleFetchError(Exception):
    """記事本文の取得・解析に失敗したことを表す例外。"""


def fetch_article_text(url: str) -> str:
    """指定したURLから記事本文を取得する。

    newspaper3kでの抽出結果が空の場合は、requests + BeautifulSoup による
    フォールバック抽出を試みる。両方失敗した場合は ArticleFetchError を送出する。
    """
    text = _fetch_with_newspaper(url)
    if text:
        return text

    logger.info("newspaper3kで本文を取得できなかったため、BeautifulSoupでフォールバックします。")
    text = _fetch_with_beautifulsoup(url)
    if text:
        return text

    raise ArticleFetchError(f"本文を取得できませんでした: {url}")


def _fetch_with_newspaper(url: str) -> str:
    try:
        article = Article(url, language="ja")
        article.download()
        article.parse()
        return article.text.strip()
    except Exception as exc:  # newspaper3kは多様な例外を投げるため広く捕捉する
        logger.warning("newspaper3kでの取得に失敗しました: %s", exc)
        return ""


def _fetch_with_beautifulsoup(url: str) -> str:
    try:
        response = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
    except requests.RequestException as exc:
        logger.warning("requestsでの取得に失敗しました: %s", exc)
        return ""

    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")]
    return "\n".join(p for p in paragraphs if p)
