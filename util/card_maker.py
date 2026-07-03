from PIL import Image, ImageDraw, ImageFont
from config.character import ChineseCharacterConfig, ChineseCharacterPhraseConfig
import const
from pathlib import Path




def _create_base_canvas(width: int, height: int) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    """步骤 1: 创建画布并绘制标准外边框"""
    image = Image.new("RGB", (width, height), const.COLOR_BACKGROUND)
    draw = ImageDraw.Draw(image)
    
    draw.rectangle(
        [const.PIXELS_OUTER_MARGIN, const.PIXELS_OUTER_MARGIN, width - const.PIXELS_OUTER_MARGIN, height - const.PIXELS_OUTER_MARGIN], 
        outline=const.COLOR_BORDER, 
        width=const.PIXELS_BORDER_WIDTH
    )
    return image, draw


def _draw_main_pinyin(draw: ImageDraw.ImageDraw, pinyin_list: list[str], font: ImageFont.FreeTypeFont, width: int, height: int) -> float:
    """步骤 2: 绘制顶部主拼音，并返回拼音文字的实际高度"""
    py_text = " ".join(pinyin_list)
    py_bbox = draw.textbbox((0, 0), py_text, font=font)
    
    py_w = py_bbox[2] - py_bbox[0]
    py_h = py_bbox[3] - py_bbox[1]
    py_y = int(height * const.RATIO_POS_MAIN_PINYIN_Y)
    
    draw.text(((width - py_w) // 2, py_y), py_text, fill=const.COLOR_MAIN_PINYIN, font=font)
    return py_h


def _draw_main_character(draw: ImageDraw.ImageDraw, character: str, font: ImageFont.FreeTypeFont, width: int, py_h: float, height: int):
    """步骤 3: 绘制中心大汉字"""
    hz_bbox = draw.textbbox((0, 0), character, font=font)
    hz_w = hz_bbox[2] - hz_bbox[0]
    
    py_y = int(height * const.RATIO_POS_MAIN_PINYIN_Y)
    hz_y = py_y + py_h + int(height * const.RATIO_POS_MAIN_GAP_Y)
    
    draw.text(((width - hz_w) // 2, hz_y), character, fill=const.COLOR_MAIN_CHARACTER, font=font)


def _draw_bottom_phrases(draw: ImageDraw.ImageDraw, phrases: list[ChineseCharacterPhraseConfig] | None, font_text: ImageFont.FreeTypeFont, font_py: ImageFont.FreeTypeFont, width: int, height: int):
    """步骤 4: 绘制底部常用词语，内部逻辑升级为【单字级中轴线对齐】（已修复汉字垂直方向不对齐BUG）"""
    bottom_boundary = int(height * const.RATIO_POS_BOTTOM_AREA_Y)
    
    # 1. 绘制底部分割线
    draw.line(
        [const.PIXELS_DIVIDER_PADDING, bottom_boundary, width - const.PIXELS_DIVIDER_PADDING, bottom_boundary], 
        fill=const.COLOR_DIVIDER, 
        width=const.PIXELS_DIVIDER_WIDTH
    )
    
    if not phrases:
        return

    num_phrases = len(phrases)
    section_width = width / num_phrases  # 整个卡片横向平分为等宽的区块
    
    for idx, pc in enumerate(phrases):
        word = pc.character_phrase                                # 字符串，如 "中国"
        pinyin_list = pc.computed_character_phrase_pinyin        # 列表, 已经转好的 ["zhōng", "guó"]
            
        # 计算当前大词组区块的几何中心轴
        section_center_x = (idx + 0.5) * section_width
        
        # --- 核心尺寸测算 ---
        # 预先获取单字的宽度。汉字是等宽的，直接取第一个字即可
        char_bbox = draw.textbbox((0, 0), word[0], font=font_text)
        char_w = char_bbox[2] - char_bbox[0]
        
        # 设定字间距
        char_spacing = int(char_w * const.RATIO_CHAR_SPACING_OF_WIDTH)
        
        # 计算整个词组在视觉上的总宽度
        total_word_len = len(word)
        total_word_width = (char_w * total_word_len) + (char_spacing * (total_word_len - 1))
        
        # 计算词组内第一个字左边缘的起始 X 坐标
        word_start_x = section_center_x - (total_word_width / 2)
        
        # 🔑 【核心修复 1】动态拼接当前词组的所有拼音作为测量样本，100% 覆盖最高点与最低点
        current_phrase_pinyin_sample = "".join(pinyin_list)
        sample_py_bbox = draw.textbbox((0, 0), current_phrase_pinyin_sample, font=font_py)
        fixed_py_h = sample_py_bbox[3] - sample_py_bbox[1]
        
        # 🔑 【核心修复 2】在进入单字绘制循环前，提前锁定所有单字拼音与汉字统一的、绝对的 Y 轴坐标
        py_pos_y = bottom_boundary + int(height * const.RATIO_POS_PHRASE_PINYIN_Y)
        word_pos_y = py_pos_y + fixed_py_h + int(height * const.RATIO_POS_PHRASE_GAP_Y)
        
        # 逐字绘制：让单字和单字拼音在各自的中轴线上完美对齐
        for i in range(total_word_len):
            single_char = word[i]
            single_py = pinyin_list[i]
            
            # 计算当前汉字的核心中轴线 X 坐标
            current_char_center_x = word_start_x + (i * (char_w + char_spacing)) + (char_w / 2)
            
            # 1. 绘制单字拼音（垂直使用固定的 py_pos_y）
            py_bbox = draw.textbbox((0, 0), single_py, font=font_py)
            py_w = py_bbox[2] - py_bbox[0]
            draw.text((current_char_center_x - py_w // 2, py_pos_y), single_py, fill=const.COLOR_PHRASE_PINYIN, font=font_py)
            
            # 2. 绘制对应的单字汉字（🔑 垂直使用统一算好的 word_pos_y，确保绝对水平对齐）
            draw.text((current_char_center_x - char_w // 2, word_pos_y), single_char, fill=const.COLOR_PHRASE_TEXT, font=font_text)

    



# ==================== 主入口函数 ====================

def draw_single_card(config: ChineseCharacterConfig, width: int = const.DEFAULT_CARD_WIDTH, output_path: Path | None=None) -> Path:
    """利用 Pillow 像素级绘制单张卡片主入口（高宽比严格为 4:3）"""
    # 1. 计算高度与加载字体
    height = int(width * const.CARD_ASPECT_RATIO_HEIGHT_SCALE)
    
    try:
        font_text = ImageFont.truetype(const.CHARACTER_FONT, int(width * const.RATIO_FONT_SIZE_MAIN_CHARACTER))
        font_pinyin = ImageFont.truetype(const.PINYIN_FONT, int(width * const.RATIO_FONT_SIZE_MAIN_PINYIN))
        font_phrase = ImageFont.truetype(const.CHARACTER_FONT, int(width * const.RATIO_FONT_SIZE_PHRASE_TEXT))
        font_phrase_py = ImageFont.truetype(const.PINYIN_FONT, int(width * const.RATIO_FONT_SIZE_PHRASE_PINYIN))
    except IOError as e:
        raise e

    # 2. 依次调用拆分后的独立功能函数
    image, draw = _create_base_canvas(width, height)
    
    py_h = _draw_main_pinyin(draw, config.computed_character_pinyin, font_pinyin, width, height)
    
    _draw_main_character(draw, config.character, font_text, width, py_h, height)
    
    _draw_bottom_phrases(draw, config.character_phrases, font_phrase, font_phrase_py, width, height)
    
    return _save_card_image(image, config.character, output_path=output_path)


def _save_card_image(image: Image.Image, character: str, output_path: Path | None = None)  -> Path:
    """内部工具函数：根据策略解析路径、验证目录并保存图片，返回最终保存的路径"""

    # 1. 确定目标文件夹
    if not output_path:
        target_dir = Path("output") / "images"
    else:
        target_dir = output_path
        # 验证传入的路径是否是一个合法且已存在的目录
        if not target_dir.is_dir():
            raise NotADirectoryError(f"错误: 传入的路径 '{output_path}' 不是一个合法或已存在的目录。")

    # 2. 确保目标目录及其中间父目录存在
    target_dir.mkdir(parents=True, exist_ok=True)

    # 3. 构造完整的文件路径并保存
    file_path = target_dir / f"{character}.png"
    image.save(file_path)
    return file_path