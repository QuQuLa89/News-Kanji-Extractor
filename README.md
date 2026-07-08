# Kanji Extractor from News (news-kanji-extractor)

ニュース記事のURLを入力すると、本文をスクレイピングして**漢字と句読点（、。）のみ**を抽出し、標準出力への表示と txt / csv / html / xlsx 形式でのファイル出力を行うシンプルなOSSツールです。

## 特徴

- `newspaper3k` による記事本文抽出を優先的に使用
- `newspaper3k` で抽出できない場合は `requests` + `BeautifulSoup` による汎用的な本文抽出にフォールバック
- 正規表現 (`re`) によりCJK統合漢字（基本領域・拡張A）と句読点（「、」「。」）のみを抽出
- 抽出結果を `txt` / `csv` / `html` / `xlsx` の4形式で保存可能（`openpyxl` でxlsx出力）
- 外部依存は最小限（`requests`, `beautifulsoup4`, `newspaper3k`, `lxml`, `openpyxl`）

## ディレクトリ構成

```
.
├── main.py                  # CLIエントリーポイント（input()でURL・出力形式を受け取る）
├── kanji_extractor/
│   ├── __init__.py
│   ├── scraper.py           # 記事本文取得（newspaper3k / requests+BeautifulSoup）
│   ├── extractor.py         # 漢字・句読点抽出ロジック（正規表現）
│   └── writer.py            # txt/csv/html/xlsx 形式でのファイル出力
├── tests/
│   ├── test_extractor.py    # 抽出ロジックのユニットテスト
│   └── test_writer.py       # ファイル出力ロジックのユニットテスト
├── conftest.py
├── pyproject.toml
├── poetry.lock
├── LICENSE
└── .gitignore
```

## 必要要件

- Python 3.10 以上
- [Poetry](https://python-poetry.org/)

## インストール

```bash
git clone https://github.com/QuQuLa89/News-Kanji-Extractor.git
cd News-Kanji-Extractor
poetry install
```

## 使い方

```bash
poetry run python main.py
```

実行後、プロンプトが表示されるのでニュース記事のURLを入力してください。続けて出力形式（`txt`/`csv`/`html`/`xlsx`）と保存先ファイルパスを入力すると、抽出結果がファイルに保存されます（出力形式を空欄のままEnterすると、ファイル保存はスキップされます）。

```
ニュース記事のURLを入力してください: https://example.com/news/article123
日本経済新聞社、東京都中央区...
出力形式を選択してください (txt/csv/html/xlsx): csv
保存先のファイルパスを入力してください (例: output.csv): result.csv
result.csv に保存しました。
```

## テスト

`pytest` は dev 依存として `pyproject.toml` に含まれているため、`poetry install` 済みであれば追加作業は不要です。

```bash
poetry run pytest
```

ネットワークアクセスを伴うスクレイピング処理自体はテスト対象外とし、抽出ロジック (`kanji_extractor/extractor.py`) とファイル出力ロジック (`kanji_extractor/writer.py`) のみを単体テストしています。

## 注意事項

- スクレイピング対象サイトの利用規約・`robots.txt` を確認し、許可された範囲でご利用ください。
- サイトによっては本文抽出の精度が低下する場合があります（`newspaper3k` のフォールバックは段落 (`<p>`) タグ単位の簡易抽出です）。
- 短時間に大量のリクエストを送信しないようご注意ください。

## ライセンス

[MIT License](LICENSE)
