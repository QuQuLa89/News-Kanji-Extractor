# Gi-Kobun-Maker（GitHub: News-Kanji-Extractor）

ニュース記事の URL から漢字と句読点（、。）のみを抽出する CLI ツール（Python）。

## コマンド

- 実行: `python main.py`（対話式で URL と出力形式を入力）
- テスト: `pytest -q`
- 依存: `pip install -r requirements.txt`（開発用は `requirements-dev.txt`）

## 構成

- `kanji_extractor/` … `scraper.py`（newspaper3k → requests+BeautifulSoup フォールバック）/ `extractor.py`（正規表現で CJK 漢字＋句読点抽出）/ `writer.py`（txt/csv/html/xlsx 出力）
- `tests/` … extractor / writer のユニットテスト
- 出力ファイル `/output.*` は gitignore 済み
