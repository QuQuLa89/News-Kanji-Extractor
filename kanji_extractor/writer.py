"""抽出結果をファイルへ出力するモジュール。"""

from __future__ import annotations

import csv
import html
from pathlib import Path

from openpyxl import Workbook

SUPPORTED_FORMATS = ("txt", "csv", "html", "xlsx")


class UnsupportedFormatError(Exception):
    """サポートされていない出力形式が指定されたことを表す例外。"""


def save_output(text: str, output_path: str | Path, fmt: str) -> Path:
    """抽出済みテキストを指定形式でファイルに保存し、保存先のパスを返す。"""
    fmt = fmt.lower()
    if fmt not in SUPPORTED_FORMATS:
        raise UnsupportedFormatError(f"未対応の出力形式です: {fmt}")

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    _WRITERS[fmt](text, path)
    return path


def _save_txt(text: str, path: Path) -> None:
    path.write_text(text, encoding="utf-8")


def _save_csv(text: str, path: Path) -> None:
    # utf-8-sig: Windows版Excelで開いた際に文字化けしないようBOMを付与する。
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["text"])
        writer.writerow([text])


def _save_html(text: str, path: Path) -> None:
    escaped = html.escape(text)
    document = (
        "<!DOCTYPE html>\n"
        '<html lang="ja">\n'
        "<head>\n"
        '  <meta charset="utf-8">\n'
        "  <title>抽出結果</title>\n"
        "</head>\n"
        "<body>\n"
        f"  <pre>{escaped}</pre>\n"
        "</body>\n"
        "</html>\n"
    )
    path.write_text(document, encoding="utf-8")


def _save_xlsx(text: str, path: Path) -> None:
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "抽出結果"
    sheet["A1"] = "text"
    sheet["A2"] = text
    workbook.save(path)


_WRITERS = {
    "txt": _save_txt,
    "csv": _save_csv,
    "html": _save_html,
    "xlsx": _save_xlsx,
}
