"""ニュース記事から漢字（および句読点）のみを抽出するCLIツール。

URLを標準入力から受け取り、本文を取得して漢字・句読点のみを抽出し、
標準出力への表示と指定形式（txt/csv/html/xlsx）でのファイル保存を行う。
"""

from __future__ import annotations

import logging
import sys

from kanji_extractor import (
    SUPPORTED_FORMATS,
    ArticleFetchError,
    UnsupportedFormatError,
    extract_kanji,
    fetch_article_text,
    save_output,
)

logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")


def main() -> int:
    url = input("ニュース記事のURLを入力してください: ").strip()
    if not url:
        print("URLが入力されませんでした。", file=sys.stderr)
        return 1

    try:
        text = fetch_article_text(url)
    except ArticleFetchError as exc:
        print(f"エラー: {exc}", file=sys.stderr)
        return 1

    kanji_text = extract_kanji(text)
    if not kanji_text:
        print("漢字を抽出できませんでした。")
        return 1

    print(kanji_text)

    formats_label = "/".join(SUPPORTED_FORMATS)
    fmt = input(f"出力形式を選択してください ({formats_label}): ").strip().lower()
    if not fmt:
        print("出力形式が入力されなかったため、ファイル保存を行いません。")
        return 0

    output_path = input(
        f"保存先のファイルパスを入力してください (例: output.{fmt}): "
    ).strip()
    if not output_path:
        output_path = f"output.{fmt}"

    try:
        saved_path = save_output(kanji_text, output_path, fmt)
    except UnsupportedFormatError as exc:
        print(f"エラー: {exc}", file=sys.stderr)
        return 1

    print(f"{saved_path} に保存しました。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
