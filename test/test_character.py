import pytest
from config.character import (
    is_valid_tone3,
    check_pinyin_invalid,
    ChineseCharacterPhraseConfig,
    ChineseCharacterConfig,
    CharacterConfigException,
)


class TestPinyinValidation:
    def test_is_valid_tone3_valid(self):
        assert is_valid_tone3("tian1") is True
        assert is_valid_tone3("kong1") is True
        assert is_valid_tone3("zhong1") is True
        assert is_valid_tone3("lü4") is True
        assert is_valid_tone3("nv3") is True

    def test_is_valid_tone3_invalid(self):
        assert is_valid_tone3("tian") is False
        assert is_valid_tone3("123") is False
        assert is_valid_tone3("tian6") is False
        assert is_valid_tone3("") is False
        assert is_valid_tone3(None) is False

    def test_check_pinyin_invalid_valid(self):
        check_pinyin_invalid(["tian1", "kong1"])

    def test_check_pinyin_invalid_invalid(self):
        with pytest.raises(CharacterConfigException):
            check_pinyin_invalid(["tian"])


class TestChineseCharacterPhraseConfig:
    def test_from_str_only_phrase(self):
        phrase = ChineseCharacterPhraseConfig.from_str("天空")
        assert phrase.character_phrase == "天空"
        assert phrase.character_phrase_pinyin is None

    def test_from_str_with_pinyin(self):
        phrase = ChineseCharacterPhraseConfig.from_str("天空@tian1#kong1")
        assert phrase.character_phrase == "天空"
        assert phrase.character_phrase_pinyin == ["tian1", "kong1"]

    def test_from_str_invalid_format(self):
        with pytest.raises(CharacterConfigException):
            ChineseCharacterPhraseConfig.from_str("天空@tian1")

    def test_from_str_invalid_pinyin(self):
        with pytest.raises(CharacterConfigException):
            ChineseCharacterPhraseConfig.from_str("天空@tian#kong1")

    def test_from_csv_str(self):
        phrase = ChineseCharacterPhraseConfig.from_csv_str("天空", "tian1 kong1")
        assert phrase.character_phrase == "天空"
        assert phrase.character_phrase_pinyin == ["tian1", "kong1"]

    def test_from_csv_str_no_pinyin(self):
        phrase = ChineseCharacterPhraseConfig.from_csv_str("天空", "")
        assert phrase.character_phrase == "天空"
        assert phrase.character_phrase_pinyin is None

    def test_from_csv_str_invalid_pinyin_count(self):
        with pytest.raises(CharacterConfigException):
            ChineseCharacterPhraseConfig.from_csv_str("天空", "tian1")


class TestChineseCharacterConfig:
    def test_from_csv_row_valid(self):
        row_dict = {
            "character": "天",
            "character_pinyin": "tian1",
            "phrases": "天空|天堂",
            "phrases_pinyin": "tian1 kong1|tian1 tang2",
        }
        config = ChineseCharacterConfig.from_csv_row(row_dict)
        assert config.character == "天"
        assert config.character_pinyin == ["tian1"]
        assert len(config.character_phrases) == 2
        assert config.character_phrases[0].character_phrase == "天空"

    def test_from_csv_row_empty_char(self):
        row_dict = {
            "character": "",
            "character_pinyin": "",
            "phrases": "",
            "phrases_pinyin": "",
        }
        with pytest.raises(CharacterConfigException):
            ChineseCharacterConfig.from_csv_row(row_dict)

    def test_from_csv_row_heteronym(self):
        row_dict = {
            "character": "行",
            "character_pinyin": "xing2|hang2",
            "phrases": "行走|银行",
            "phrases_pinyin": "xing2 zou3|yin2 hang2",
        }
        config = ChineseCharacterConfig.from_csv_row(row_dict)
        assert config.character == "行"
        assert config.character_pinyin == ["xing2", "hang2"]

    def test_computed_character_pinyin_with_pinyin(self):
        config = ChineseCharacterConfig("天", character_pinyin=["tian1"])
        assert "tiān" in config.computed_character_pinyin

    def test_computed_character_pinyin_auto(self):
        config = ChineseCharacterConfig("天")
        assert "tiān" in config.computed_character_pinyin
