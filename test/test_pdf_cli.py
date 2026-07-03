import pytest
from typer.testing import CliRunner
from main import app
from pathlib import Path

runner = CliRunner()


class TestPdfExportCommand:
    def test_help(self):
        result = runner.invoke(app, ["pdf", "export", "--help"])
        assert result.exit_code == 0
        assert "将卡片图片导出为 PDF" in result.output

    def test_invalid_output_path_is_directory(self, tmp_path):
        output_path = tmp_path / "mydir"
        output_path.mkdir()
        result = runner.invoke(
            app, ["pdf", "export", "-i", str(tmp_path), "-o", str(output_path)]
        )
        assert result.exit_code != 0
        assert "是一个目录" in result.output

    def test_invalid_file_extension(self, tmp_path):
        output_path = tmp_path / "cards.txt"
        result = runner.invoke(
            app, ["pdf", "export", "-i", str(tmp_path), "-o", str(output_path)]
        )
        assert result.exit_code != 0
        assert "非法的目标格式" in result.output

    def test_missing_images_dir(self):
        result = runner.invoke(
            app, ["pdf", "export", "-i", "/nonexistent/images", "-o", "/tmp/cards.pdf"]
        )
        assert result.exit_code != 0

    def test_valid_export(self, tmp_path):
        from util.card_maker import draw_single_card
        from config.character import ChineseCharacterConfig

        image_dir = tmp_path / "images"
        image_dir.mkdir()

        config = ChineseCharacterConfig("天")
        draw_single_card(config, width=200, output_path=image_dir)

        output_pdf = tmp_path / "cards.pdf"
        result = runner.invoke(
            app, ["pdf", "export", "-i", str(image_dir), "-o", str(output_pdf), "-n", 1]
        )
        assert result.exit_code == 0
        assert output_pdf.exists()
        assert output_pdf.stat().st_size > 0

    def test_output_directory_created(self, tmp_path):
        from util.card_maker import draw_single_card
        from config.character import ChineseCharacterConfig

        image_dir = tmp_path / "images"
        image_dir.mkdir()

        config = ChineseCharacterConfig("天")
        draw_single_card(config, width=200, output_path=image_dir)

        output_pdf = tmp_path / "new_dir" / "sub_dir" / "cards.pdf"
        assert not output_pdf.parent.exists()

        result = runner.invoke(
            app, ["pdf", "export", "-i", str(image_dir), "-o", str(output_pdf), "-n", 1]
        )
        assert result.exit_code == 0
        assert output_pdf.exists()
        assert output_pdf.parent.exists()

    def test_nums_per_page_options(self, tmp_path):
        from util.card_maker import draw_single_card
        from config.character import ChineseCharacterConfig

        image_dir = tmp_path / "images"
        image_dir.mkdir()

        for char in ["天", "地", "人", "行"]:
            config = ChineseCharacterConfig(char)
            draw_single_card(config, width=200, output_path=image_dir)

        for nums in [1, 2, 3, 4]:
            output_pdf = tmp_path / f"cards_{nums}.pdf"
            result = runner.invoke(
                app,
                [
                    "pdf",
                    "export",
                    "-i",
                    str(image_dir),
                    "-o",
                    str(output_pdf),
                    "-n",
                    nums,
                ],
            )
            assert result.exit_code == 0
            assert output_pdf.exists()
