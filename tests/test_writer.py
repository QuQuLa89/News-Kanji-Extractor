"""kanji_extractor.writer のユニットテスト。"""

import csv

import pytest
from openpyxl import load_workbook

from kanji_extractor.writer import UnsupportedFormatError, save_output

SAMPLE_TEXT = "今日、天気良。"


def test_save_txt(tmp_path) -> None:
    path = save_output(SAMPLE_TEXT, tmp_path / "out.txt", "txt")
    assert path.read_text(encoding="utf-8") == SAMPLE_TEXT


def test_save_csv(tmp_path) -> None:
    path = save_output(SAMPLE_TEXT, tmp_path / "out.csv", "csv")
    with path.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.reader(f))
    assert rows == [["text"], [SAMPLE_TEXT]]


def test_save_html(tmp_path) -> None:
    path = save_output(SAMPLE_TEXT, tmp_path / "out.html", "html")
    content = path.read_text(encoding="utf-8")
    assert SAMPLE_TEXT in content
    assert content.startswith("<!DOCTYPE html>")


def test_save_xlsx(tmp_path) -> None:
    path = save_output(SAMPLE_TEXT, tmp_path / "out.xlsx", "xlsx")
    workbook = load_workbook(path)
    sheet = workbook.active
    assert sheet["A1"].value == "text"
    assert sheet["A2"].value == SAMPLE_TEXT


def test_save_output_unsupported_format(tmp_path) -> None:
    with pytest.raises(UnsupportedFormatError):
        save_output(SAMPLE_TEXT, tmp_path / "out.pdf", "pdf")


def test_save_output_creates_parent_directories(tmp_path) -> None:
    target = tmp_path / "nested" / "dir" / "out.txt"
    path = save_output(SAMPLE_TEXT, target, "txt")
    assert path.exists()
