from reportlab.lib.pagesizes import A4
from config.config_loader import get_config_value
from util.resource_path import get_resource_path

# ==================== 卡片绘图常量配置 ====================
# 画面尺寸与比例
CARD_ASPECT_RATIO_HEIGHT_SCALE = get_config_value("cardAspectRatioHeightScale", 4 / 3)

# 颜色配置 (HEX 格式)
COLOR_BACKGROUND = get_config_value("colorBackground", "#FFFFFF")
COLOR_BORDER = get_config_value("colorBorder", "#E0E0E0")
COLOR_DIVIDER = get_config_value("colorDivider", "#E0E0E0")
COLOR_MAIN_PINYIN = get_config_value("colorMainPinyin", "#4A4A4A")
COLOR_MAIN_CHARACTER = get_config_value("colorMainCharacter", "#1A1A1A")
COLOR_PHRASE_PINYIN = get_config_value("colorPhrasePinyin", "#767676")
COLOR_PHRASE_TEXT = get_config_value("colorPhraseText", "#2B2B2B")

# 边界、线条与排版间距 (基于宽度的相对比例或固定像素)
PIXELS_OUTER_MARGIN = get_config_value("pixelsOuterMargin", 20)
PIXELS_BORDER_WIDTH = get_config_value("pixelsBorderWidth", 6)
PIXELS_DIVIDER_WIDTH = get_config_value("pixelsDividerWidth", 2)
PIXELS_DIVIDER_PADDING = get_config_value("pixelsDividerPadding", 40)

RATIO_FONT_SIZE_MAIN_CHARACTER = get_config_value("ratioFontSizeMainCharacter", 0.6)
RATIO_FONT_SIZE_MAIN_PINYIN = get_config_value("ratioFontSizeMainPinyin", 0.12)
RATIO_FONT_SIZE_PHRASE_TEXT = get_config_value("ratioFontSizePhraseText", 0.12)
RATIO_FONT_SIZE_PHRASE_PINYIN = get_config_value("ratioFontSizePhrasePinyin", 0.035)

# 垂直纵向布局占比 (基于高度的比例)
RATIO_POS_MAIN_PINYIN_Y = get_config_value("ratioPosMainPinyinY", 0.12)
RATIO_POS_MAIN_GAP_Y = get_config_value("ratioPosMainGapY", 0.05)
RATIO_POS_BOTTOM_AREA_Y = get_config_value("ratioPosBottomAreaY", 0.8)
RATIO_POS_PHRASE_PINYIN_Y = get_config_value("ratioPosPhrasePinyinY", 0.03)
RATIO_POS_PHRASE_GAP_Y = get_config_value("ratioPosPhraseGapY", 0.01)
COEFFICIENT_GRID_CENTER_WEIGHT = get_config_value("coefficientGridCenterWeight", 0.5)
RATIO_CHAR_SPACING_OF_WIDTH = get_config_value("ratioCharSpacingOfWidth", 0.1)

_character_font_value = get_config_value("characterFont", None)
if _character_font_value:
    CHARACTER_FONT = str(get_resource_path(_character_font_value))
else:
    CHARACTER_FONT = str(get_resource_path("fonts/FZKTK.TTF"))

_pinyin_font_value = get_config_value("pinyinFont", None)
if _pinyin_font_value:
    PINYIN_FONT = str(get_resource_path(_pinyin_font_value))
else:
    PINYIN_FONT = str(get_resource_path("fonts/msyh.ttc"))
DEFAULT_CARD_WIDTH = get_config_value("defaultCardWidth", 1200)


# ==================== PDF 拼版常量配置 ====================
PDF_PAGE_SIZE = A4
PDF_MARGIN_X = get_config_value("pdfMarginX", 30)
PDF_MARGIN_Y = get_config_value("pdfMarginY", 40)

CARD_IMAGE_ASPECT_RATIO = get_config_value("cardImageAspectRatio", 1200 / 1600)
CARD_GRID_SCALE_FACTOR = get_config_value("cardGridScaleFactor", 0.95)

COLOR_TRIM_LINE = get_config_value("colorTrimLine", "#D0D0D0")
WIDTH_TRIM_LINE = get_config_value("widthTrimLine", 0.5)
DASH_PATTERN_TRIM_LINE = get_config_value("dashPatternTrimLine", [4.0, 4.0])

GRID_LAYOUT_MAP = {1: (1, 1), 2: (2, 1), 3: (3, 1), 4: (2, 2)}
DEFAULT_GRID_LAYOUT = (2, 2)

DEFAULT_IMAGE_NUMS_PER_PAGE = get_config_value("defaultImageNumsPerPage", 2)

ROTATION_ANGLE_DEGREES = get_config_value("rotationAngleDegrees", -90)
