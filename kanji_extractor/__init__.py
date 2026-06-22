"""ニュース記事本文から漢字のみを抽出するためのパッケージ。"""

from .extractor import extract_kanji
from .scraper import ArticleFetchError, fetch_article_text
from .writer import SUPPORTED_FORMATS, UnsupportedFormatError, save_output

__version__ = "0.2.0"
__all__ = [
    "extract_kanji",
    "fetch_article_text",
    "ArticleFetchError",
    "save_output",
    "SUPPORTED_FORMATS",
    "UnsupportedFormatError",
]
