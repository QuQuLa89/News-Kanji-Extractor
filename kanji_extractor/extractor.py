"""テキストから漢字（および句読点）のみを抽出するモジュール。"""

from __future__ import annotations

import re

# CJK統合漢字（基本領域: U+4E00-U+9FFF）と拡張A（U+3400-U+4DBF）、
# および句読点の「、」（U+3001）「。」（U+3002）を対象範囲とする。
_KANJI_PATTERN = re.compile(r"[一-鿿㐀-䶿、。]")


def extract_kanji(text: str) -> str:
    """テキストから漢字と句読点（、。）のみを抜き出し、連結した文字列を返す。"""
    return "".join(_KANJI_PATTERN.findall(text))
