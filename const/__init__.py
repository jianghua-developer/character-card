from reportlab.lib.pagesizes import A4
from config.config_loader import get_config_value
from util.resource_path import get_resource_path

# ==================== 卡片绘图常量配置 ====================
# 画面尺寸与比例
CARD_ASPECT_RATIO_HEIGHT_SCALE = get_config_value(
    "cardAspectRatioHeightScale", 4 / 3
)  # 卡片高度与宽度的比例（高/宽）

# 颜色配置 (HEX 格式)
COLOR_BACKGROUND = get_config_value("colorBackground", "#FFFFFF")  # 卡片背景颜色
COLOR_BORDER = get_config_value("colorBorder", "#E0E0E0")  # 卡片外边框颜色
COLOR_DIVIDER = get_config_value(
    "colorDivider", "#E0E0E0"
)  # 主汉字与词组区域之间的分隔线颜色
COLOR_MAIN_PINYIN = get_config_value("colorMainPinyin", "#4A4A4A")  # 主汉字拼音的颜色
COLOR_MAIN_CHARACTER = get_config_value("colorMainCharacter", "#1A1A1A")  # 主汉字的颜色
COLOR_PHRASE_PINYIN = get_config_value("colorPhrasePinyin", "#767676")  # 词组拼音的颜色
COLOR_PHRASE_TEXT = get_config_value("colorPhraseText", "#2B2B2B")  # 词组文字的颜色

# 边界、线条与排版间距 (基于宽度的相对比例或固定像素)
PIXELS_OUTER_MARGIN = get_config_value(
    "pixelsOuterMargin", 20
)  # 卡片内容区域与边框之间的外边距（像素）
PIXELS_BORDER_WIDTH = get_config_value("pixelsBorderWidth", 6)  # 卡片外边框宽度（像素）
PIXELS_DIVIDER_WIDTH = get_config_value("pixelsDividerWidth", 2)  # 分隔线宽度（像素）
PIXELS_DIVIDER_PADDING = get_config_value(
    "pixelsDividerPadding", 40
)  # 分隔线与上下内容的间距（像素）

RATIO_FONT_SIZE_MAIN_CHARACTER = get_config_value(
    "ratioFontSizeMainCharacter", 0.6
)  # 主汉字字体大小占卡片宽度的比例
RATIO_FONT_SIZE_MAIN_PINYIN = get_config_value(
    "ratioFontSizeMainPinyin", 0.12
)  # 主汉字拼音字体大小占卡片宽度的比例
RATIO_FONT_SIZE_PHRASE_TEXT = get_config_value(
    "ratioFontSizePhraseText", 0.12
)  # 词组文字字体大小占卡片宽度的比例
RATIO_FONT_SIZE_PHRASE_PINYIN = get_config_value(
    "ratioFontSizePhrasePinyin", 0.035
)  # 词组拼音字体大小占卡片宽度的比例

# 垂直纵向布局占比 (基于高度的比例)
RATIO_POS_MAIN_PINYIN_Y = get_config_value(
    "ratioPosMainPinyinY", 0.12
)  # 主汉字拼音垂直位置占卡片高度的比例
RATIO_POS_MAIN_GAP_Y = get_config_value(
    "ratioPosMainGapY", 0.05
)  # 主汉字拼音与主汉字之间的垂直间距比例
RATIO_POS_BOTTOM_AREA_Y = get_config_value(
    "ratioPosBottomAreaY", 0.8
)  # 词组区域顶部位置占卡片高度的比例
RATIO_POS_PHRASE_PINYIN_Y = get_config_value(
    "ratioPosPhrasePinyinY", 0.03
)  # 词组拼音与词组文字之间的垂直间距比例
RATIO_POS_PHRASE_GAP_Y = get_config_value(
    "ratioPosPhraseGapY", 0.01
)  # 多个词组之间的垂直间距比例
COEFFICIENT_GRID_CENTER_WEIGHT = get_config_value(
    "coefficientGridCenterWeight", 0.5
)  # 主汉字网格居中权重系数（0-1）
RATIO_CHAR_SPACING_OF_WIDTH = get_config_value(
    "ratioCharSpacingOfWidth", 0.1
)  # 多音字拼音之间的字间距占卡片宽度的比例

# 字体配置
_character_font_value = get_config_value("characterFont", None)
if _character_font_value:
    CHARACTER_FONT = str(get_resource_path(_character_font_value))  # 汉字字体文件路径
else:
    CHARACTER_FONT = str(get_resource_path("fonts/FZKTK.TTF"))

_pinyin_font_value = get_config_value("pinyinFont", None)
if _pinyin_font_value:
    PINYIN_FONT = str(get_resource_path(_pinyin_font_value))  # 拼音字体文件路径
else:
    PINYIN_FONT = str(get_resource_path("fonts/msyh.ttc"))

DEFAULT_CARD_WIDTH = get_config_value("defaultCardWidth", 1200)  # 默认卡片宽度（像素）


# ==================== PDF 拼版常量配置 ====================
PDF_PAGE_SIZE = A4  # PDF 页面尺寸

PDF_MARGIN_X = get_config_value("pdfMarginX", 30)  # PDF 页面水平边距（点）
PDF_MARGIN_Y = get_config_value("pdfMarginY", 40)  # PDF 页面垂直边距（点）

CARD_IMAGE_ASPECT_RATIO = get_config_value(
    "cardImageAspectRatio", 1200 / 1600
)  # 卡片图片宽高比（宽/高）
CARD_GRID_SCALE_FACTOR = get_config_value(
    "cardGridScaleFactor", 0.95
)  # 卡片在 PDF 网格中的缩放系数

COLOR_TRIM_LINE = get_config_value("colorTrimLine", "#D0D0D0")  # 裁剪虚线颜色
WIDTH_TRIM_LINE = get_config_value("widthTrimLine", 0.5)  # 裁剪虚线宽度（点）
DASH_PATTERN_TRIM_LINE = get_config_value(
    "dashPatternTrimLine", [4.0, 4.0]
)  # 裁剪虚线的虚实间隔模式

GRID_LAYOUT_MAP = {
    1: (1, 1),
    2: (2, 1),
    3: (3, 1),
    4: (2, 2),
}  # 每页卡片数对应的网格布局映射
DEFAULT_GRID_LAYOUT = (2, 2)  # 默认网格布局

DEFAULT_IMAGE_NUMS_PER_PAGE = get_config_value(
    "defaultImageNumsPerPage", 2
)  # 默认每页 PDF 中的卡片数量

ROTATION_ANGLE_DEGREES = get_config_value(
    "rotationAngleDegrees", -90
)  # 卡片在 PDF 中的旋转角度（度），负数表示逆时针旋转
