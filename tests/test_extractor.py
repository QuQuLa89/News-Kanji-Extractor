"""kanji_extractor.extractor のユニットテスト。"""

from kanji_extractor.extractor import extract_kanji


def test_extract_kanji_from_mixed_text() -> None:
    text = "今日はThe天気が良いです123。"
    assert extract_kanji(text) == "今日天気良。"


def test_extract_kanji_with_no_kanji() -> None:
    assert extract_kanji("Hello, world! 123 ひらがな") == ""


def test_extract_kanji_with_empty_string() -> None:
    assert extract_kanji("") == ""


def test_extract_kanji_with_only_kanji() -> None:
    assert extract_kanji("日本語勉強") == "日本語勉強"


def test_extract_kanji_includes_punctuation() -> None:
    text = "今日は、天気が良い。明日も、晴れるだろう。"
    assert extract_kanji(text) == "今日、天気良。明日、晴。"
