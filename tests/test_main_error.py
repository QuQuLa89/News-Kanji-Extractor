"""main.py の例外ハンドリングテスト。"""

from unittest.mock import patch

from main import main


def test_main_handles_oserror() -> None:
    with (
        patch(
            "builtins.input", side_effect=["https://example.com/test", "txt", "out.txt"]
        ),
        patch("main.fetch_article_text", return_value="今日は晴れです。"),
        patch("main.save_output", side_effect=PermissionError("Permission denied")),
    ):
        code = main()
        assert code == 1
