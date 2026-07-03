import pytest
from typer.testing import CliRunner
from main import app

runner = CliRunner()


class TestCardGenerateCommand:
    def test_help(self):
        result = runner.invoke(app, ["card", "generate", "--help"])
        assert result.exit_code == 0
        assert "生成汉字卡片图片" in result.output

    def test_no_args(self):
        result = runner.invoke(app, ["card", "generate"])
        assert "没有找到配置" in result.output

    def test_char_and_config_conflict(self, mock_confirm):
        result = runner.invoke(
            app, ["card", "generate", "-c", "天", "--config", "/nonexistent.csv"]
        )
        assert "不能同时配置" in result.output

    def test_single_char(self, tmp_path, mock_confirm):
        output_dir = tmp_path / "cards"
        result = runner.invoke(
            app, ["card", "generate", "-c", "天", "-o", str(output_dir), "-w", 200]
        )
        assert result.exit_code == 0
        assert output_dir.exists()
        assert len(list(output_dir.glob("*.png"))) == 1

    def test_char_with_pinyin(self, tmp_path, mock_confirm):
        output_dir = tmp_path / "cards"
        result = runner.invoke(
            app,
            ["card", "generate", "-c", "天:tian1", "-o", str(output_dir), "-w", 200],
        )
        assert result.exit_code == 0
        assert output_dir.exists()
        assert len(list(output_dir.glob("*.png"))) == 1

    def test_char_with_phrases(self, tmp_path, mock_confirm):
        output_dir = tmp_path / "cards"
        result = runner.invoke(
            app,
            [
                "card",
                "generate",
                "-c",
                "天:tian1:天空@tian1#kong1",
                "-o",
                str(output_dir),
                "-w",
                200,
            ],
        )
        assert result.exit_code == 0
        assert output_dir.exists()
        assert len(list(output_dir.glob("*.png"))) == 1

    def test_invalid_pinyin(self):
        result = runner.invoke(app, ["card", "generate", "-c", "天:tian"])
        assert result.exit_code != 0
        assert "invalid pinyin" in result.output.lower()

    def test_output_directory_created(self, tmp_path, mock_confirm):
        output_dir = tmp_path / "new_dir" / "sub_dir"
        assert not output_dir.exists()
        result = runner.invoke(
            app, ["card", "generate", "-c", "天", "-o", str(output_dir), "-w", 200]
        )
        assert result.exit_code == 0
        assert output_dir.exists()

    def test_multiple_chars(self, tmp_path, mock_confirm):
        output_dir = tmp_path / "cards"
        result = runner.invoke(
            app,
            [
                "card",
                "generate",
                "-c",
                "天:tian1",
                "-c",
                "地:di4",
                "-o",
                str(output_dir),
                "-w",
                200,
            ],
        )
        assert result.exit_code == 0
        assert output_dir.exists()
        assert len(list(output_dir.glob("*.png"))) == 2

    def test_config_file(self, tmp_path, test_csv_path, mock_confirm):
        output_dir = tmp_path / "cards"
        result = runner.invoke(
            app,
            [
                "card",
                "generate",
                "--config",
                str(test_csv_path),
                "-o",
                str(output_dir),
                "-w",
                200,
            ],
        )
        assert result.exit_code == 0
        assert output_dir.exists()
        assert len(list(output_dir.glob("*.png"))) == 5

    def test_config_file_with_range(self, tmp_path, test_csv_path, mock_confirm):
        output_dir = tmp_path / "cards"
        result = runner.invoke(
            app,
            [
                "card",
                "generate",
                "--config",
                str(test_csv_path),
                "--start",
                "1",
                "--end",
                "2",
                "-o",
                str(output_dir),
                "-w",
                200,
            ],
        )
        assert result.exit_code == 0
        assert output_dir.exists()
        assert len(list(output_dir.glob("*.png"))) == 2
