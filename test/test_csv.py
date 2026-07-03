import pytest
from pathlib import Path
from util.csv import load_configs_from_csv
from config.character import ChineseCharacterConfig


class TestLoadConfigsFromCsv:
    def test_file_not_found(self):
        csv_path = Path("/nonexistent/path/to/file.csv")
        with pytest.raises(FileNotFoundError):
            list(load_configs_from_csv(csv_path))

    def test_is_directory(self, tmp_path):
        csv_path = tmp_path / "mydir"
        csv_path.mkdir()
        with pytest.raises(IsADirectoryError):
            list(load_configs_from_csv(csv_path))

    def test_missing_columns(self, tmp_path):
        csv_path = tmp_path / "invalid.csv"
        csv_path.write_text("col1,col2\nval1,val2")
        with pytest.raises(Exception):
            list(load_configs_from_csv(csv_path))

    def test_valid_csv(self, test_csv_path):
        configs = list(load_configs_from_csv(test_csv_path))
        assert len(configs) == 5
        assert all(isinstance(c, ChineseCharacterConfig) for c in configs)
        assert configs[0].character == "天"
        assert configs[1].character == "地"

    def test_with_range(self, test_csv_path):
        configs = list(load_configs_from_csv(test_csv_path, start_row=1, end_row=3))
        assert len(configs) == 3
        assert configs[0].character == "天"
        assert configs[1].character == "地"
        assert configs[2].character == "人"

    def test_start_end_none_validation(self, test_csv_path):
        with pytest.raises(ValueError):
            list(load_configs_from_csv(test_csv_path, start_row=1))

    def test_start_greater_than_end(self, test_csv_path):
        configs = list(load_configs_from_csv(test_csv_path, start_row=3, end_row=1))
        assert len(configs) == 3
        assert configs[0].character == "天"

    def test_empty_rows_skipped(self, tmp_path):
        csv_path = tmp_path / "with_empty.csv"
        csv_path.write_text(
            "character,character_pinyin,phrases,phrases_pinyin\n"
            "天,tian1,,\n"
            ",,,\n"
            "地,di4,,\n"
        )
        configs = list(load_configs_from_csv(csv_path))
        assert len(configs) == 2
        assert configs[0].character == "天"
        assert configs[1].character == "地"
