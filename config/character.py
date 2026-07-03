import re
from dataclasses import dataclass
from pypinyin.contrib.tone_convert import tone3_to_tone
from pypinyin import pinyin

class CharacterConfigException(Exception):
    pass

def is_valid_tone3(pinyin_str: str) -> bool:
    if not pinyin_str or not isinstance(pinyin_str, str):
        return False
    
    pattern = r"^[a-züv]+[0-5]$"
    
    return bool(re.match(pattern, pinyin_str.strip().lower()))

def check_pinyin_invalid(pinyin_strs: list[str]):
    for p in pinyin_strs:
        if not is_valid_tone3(p):
            raise CharacterConfigException(f"invalid pinyin config:{p}")

@dataclass
class ChineseCharacterPhraseConfig:
    character_phrase: str 
    character_phrase_pinyin: list[str] | None = None
    
    @classmethod
    def from_str(cls, character_phrases_config_str: str) -> "ChineseCharacterPhraseConfig":
        configs = character_phrases_config_str.split("@")
        
        if len(configs) == 1:
            character_phrase = configs[0]
            return cls(character_phrase)
        
        if len(configs) == 2:
            character_phrase, character_phrase_pinyin_str = configs
            character_phrase_pinyin = character_phrase_pinyin_str.split("#")
            if len(character_phrase_pinyin) != len(character_phrase):
                raise CharacterConfigException(f"invalid character config:{character_phrase_pinyin_str}与{character_phrase}不匹配")
            
            check_pinyin_invalid(character_phrase_pinyin)
            
            return cls(character_phrase, character_phrase_pinyin = character_phrase_pinyin)
        
        raise CharacterConfigException(f"invalid character config:{character_phrases_config_str}格式不正确；示例：天空@tian1#kong1,天堂@tian1#tang2")
    
    @classmethod
    def from_csv_str(cls, phrase_str: str, pinyin_str: str) -> "ChineseCharacterPhraseConfig":
        """
        专门对接 CSV 单元格的实例化方法。
        支持传入单个词语（如 "中国"）和对应的以空格隔开的字拼音串（如 "zhong2 guo2"）。
        """
        phrase = phrase_str.strip()
        if not phrase:
            raise CharacterConfigException("invalid csv config: 词组文本不能为空")
            
        py_str = pinyin_str.strip() if pinyin_str else ""
        if not py_str:
            return cls(phrase)
            
        # 词组内部的汉字读音依旧按照行业标准使用空格隔开
        py_list = py_str.split()
        if len(py_list) != len(phrase):
            raise CharacterConfigException(f"invalid csv config: 拼音 '{py_str}' 与词组 '{phrase}' 长度不匹配")
            
        check_pinyin_invalid(py_list)
        return cls(phrase, character_phrase_pinyin=py_list)
    
    @property
    def computed_character_phrase_pinyin(self) -> list[str]:
        if self.character_phrase_pinyin:
            return [tone3_to_tone(s) for s in self.character_phrase_pinyin]
        
        character_phrase_pinyins = pinyin(self.character_phrase)
        result = []
        for p in character_phrase_pinyins:
            result.extend(p)
        return result
    
    def __str__(self) -> str:
        return f"{self.character_phrase}({self.computed_character_phrase_pinyin})"
    
    def __repr__(self) -> str:
        return self.__str__()
        


@dataclass
class ChineseCharacterConfig:
    
    character: str
    character_pinyin: list[str] | None = None
    character_phrases: list[ChineseCharacterPhraseConfig] | None = None
        
    def __str__(self) -> str:
        return f"character: {self.character} \t pinyin: {self.character_pinyin} \t phrases: {self.character_phrases} \t computed_pinyin: {self.computed_character_pinyin}"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    @property
    def computed_character_pinyin(self):
        if self.character_pinyin:
            return [tone3_to_tone(s) for s in self.character_pinyin]
        
        return pinyin(self.character, heteronym=True)[0]
    
    
    @classmethod
    def from_csv_row(cls, row_dict: dict) -> "ChineseCharacterConfig":
        """
        核心重构工厂：将 Polars 解析出的行字典转化为完整字卡配置实例。
        主汉字多音字、多组词组均统一使用 "|" 符号进行切分。
        """
        # 1. 提取并清洗主汉字，防御 Polars 的 Null 值导致转为 "None" 的问题
        char_val = row_dict.get("character")
        char = str(char_val).strip() if char_val is not None else ""
        if not char:
            raise CharacterConfigException("invalid csv row: 主汉字不能为空")

        # 2. 统一改用 "|" 符号解析主汉字多音字拼音
        py_val = row_dict.get("character_pinyin")
        raw_py = str(py_val).strip() if py_val is not None else ""
        
        # 严格使用 "|" 进行切分，清洗多余空格，并过滤掉空项
        char_py = [p.strip() for p in raw_py.split("|") if p.strip()] if raw_py else None
        
        if char_py:
            check_pinyin_invalid(char_py)

        # 3. 解析多组常用词组（同样统一使用 "|" 进行扁平化切割）
        phrase_val = row_dict.get("phrases")
        raw_phrases = str(phrase_val).strip() if phrase_val is not None else ""
        
        phrase_py_val = row_dict.get("phrases_pinyin")
        raw_phrases_py = str(phrase_py_val).strip() if phrase_py_val is not None else ""

        phrase_configs = None
        if raw_phrases:
            phrase_configs = []
            # 切分多个常用词组
            words = [w.strip() for w in raw_phrases.split("|") if w.strip()]
            # 同步切分对应的词组拼音
            pinyins = [p.strip() for p in raw_phrases_py.split("|")] if raw_phrases_py else []
            
            for idx, word in enumerate(words):
                current_py = pinyins[idx] if idx < len(pinyins) else ""
                # 调用 PhraseConfig 的 CSV 特化解析方法
                phrase_cfg = ChineseCharacterPhraseConfig.from_csv_str(word, current_py)
                phrase_configs.append(phrase_cfg)

        return cls(character=char, character_pinyin=char_py, character_phrases=phrase_configs)
    
        
if __name__ == "__main__":
    pass
    