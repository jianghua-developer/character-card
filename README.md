# Character Card Generator

一个基于 Python 的命令行工具，用于快速生成汉字学习卡片和将多张卡片拼版导出为 PDF 文件。

## ✨ 功能特性

- 支持手动指定拼音或自动注音（解决多音字问题）
- 批量处理：通过 CSV 文件导入，支持大文件流式解析
- 精美排版：卡片包含主汉字、拼音、常用词组
- 灵活输出：自定义卡片尺寸，支持多种 PDF 拼版布局
- 打印友好：自动添加裁剪虚线，方便打印裁剪

## 🛠️ 技术栈

| 依赖库           | 版本      | 用途                    |
| ------------- | ------- | --------------------- |
| **typer**     | ≥0.26.8 | 命令行界面框架（含 rich 终端富文本） |
| **Pillow**    | ≥12.3.0 | 卡片图片绘制                |
| **reportlab** | ≥5.0.0  | PDF 拼版导出              |
| **pypinyin**  | ≥0.55.0 | 汉字自动注音                |
| **polars**    | ≥1.42.1 | 高性能 CSV 解析（Rust 实现）   |

## 📁 项目结构

```
character-card/
├── main.py              # 入口文件，注册子命令
├── pyproject.toml       # 项目依赖配置
├── character-card.spec  # PyInstaller 打包配置
├── fonts/               # 字体资源
│   ├── FZKTK.TTF        # 汉字字体（方正卡通体）
│   └── msyh.ttc         # 拼音字体（微软雅黑）
├── const/               # 常量配置
│   └── __init__.py      # 绘图和拼版参数
├── config/              # 配置解析
│   ├── character.py     # 汉字配置数据结构
│   └── config_loader.py # 配置文件加载器
├── subcommand/          # 子命令
│   ├── card.py          # 卡片生成子命令
│   └── pdf.py           # PDF 导出子命令
├── util/                # 工具模块
│   ├── card_maker.py    # 卡片绘制逻辑
│   ├── pdf_maker.py     # PDF 拼版逻辑
│   ├── csv.py           # CSV 配置加载逻辑
│   └── resource_path.py # 资源路径解析工具（兼容打包模式）
└── scripts/             # 脚本
    └── build.sh         # Linux/macOS 一键打包脚本
```

## 🚀 快速开始

### 环境要求

- **Python**: ≥3.12
- **包管理器**: uv

### 安装依赖

```bash
uv sync
```

### 激活虚拟环境

**Unix/Linux/macOS**:

```bash
source .venv/bin/activate
```

**Windows**:

```powershell
.venv\Scripts\activate
```

## 📖 命令行使用指南

### 1. 生成卡片图片

```bash
python main.py card generate [选项]
```

#### 方式一：命令行直接配置

```bash
# 单个汉字（自动注音）
python main.py card generate -c 天

# 单个汉字 + 手动指定拼音
python main.py card generate -c 天:tian1

# 单个汉字 + 拼音 + 词组
python main.py card generate -c 天:tian1:天空@tian1#kong1,天堂@tian1#tang2

# 多个汉字
python main.py card generate -c 天:tian1 -c 空:kong1
```

#### 方式二：CSV 配置文件批量生成

```bash
# 生成全部配置
python main.py card generate --config config.csv

# 指定行范围（第1-10行）
python main.py card generate --config config.csv --start 1 --end 10
```

#### 参数说明

| 参数               | 说明                    | 默认值              |
| ---------------- | --------------------- | ---------------- |
| `-c/--character` | 汉字配置，格式见下文            | -                |
| `-w/--width`     | 卡片宽度（像素）              | 1200             |
| `-o/--output`    | 输出目录                  | `output/images/` |
| `--config`       | CSV 配置文件路径            | -                |
| `--start`        | 起始行（配合 `--config` 使用） | -                |
| `--end`          | 结束行（配合 `--config` 使用） | -                |

#### 使用注意事项

- **参数互斥**：`--character` 和 `--config` 不能同时使用
- **确认提示**：使用 `--character` 方式时，程序会显示拼音配置预览并询问确认，输入 `y` 后才会生成图片

### 2. 导出 PDF

```bash
python main.py pdf export [选项]
```

#### 基本用法

```bash
# 默认每页 2 张卡片
python main.py pdf export --images ./output/images --output ./output/cards.pdf

# 指定每页 4 张卡片
python main.py pdf export -i ./output/images -o ./output/cards.pdf -n 4
```

#### 参数说明

| 参数            | 说明             | 默认值    |
| ------------- | -------------- | ------ |
| `-i/--images` | PNG 图片目录路径     | **必填** |
| `-o/--output` | PDF 文件输出路径     | **必填** |
| `-n/--nums`   | 每页卡片数（1/2/3/4） | 2      |

## 📋 配置格式说明

### 命令行配置格式

```
汉字:拼音1,拼音2:词组1@拼音#拼音,词组2@拼音#拼音
```

**规则**：

- 用 `:` 分隔汉字、拼音、词组三部分
- 多音字用 `,` 分隔
- 多词组用 `,` 分隔
- 词组内用 `@` 分隔词组和拼音
- 词组拼音内用 `#` 分隔每个字的拼音

**示例**：

```
天:tian1:天空@tian1#kong1,天堂@tian1#tang2
行:xing2,hang2:行走@xing2#zou3,银行@yin2#hang2
```

### CSV 配置文件格式

**表头**：`character`, `character_pinyin`, `phrases`, `phrases_pinyin`

**规则**：

- 多音字用 `|` 分隔
- 多词组用 `|` 分隔
- 词组拼音内用**空格**分隔

**示例**：

| character | character\_pinyin | phrases | phrases\_pinyin          |
| --------- | ----------------- | ------- | ------------------------ |
| 天         | tian1             | 天空\|天堂  | tian1 kong1\|tian1 tang2 |
| 行         | xing2\|hang2      | 行走\|银行  | xing2 zou3\|yin2 hang2   |
| 好         | hao3\|hao4        | 好人\|爱好  | hao3 ren2\|ai4 hao4      |

## 📐 PDF 拼版布局

| 每页卡片数 | 网格布局 | 旋转策略      | 适用场景  |
| ----- | ---- | --------- | ----- |
| 1     | 1×1  | 不旋转       | 大尺寸展示 |
| 2     | 2×1  | **旋转90°** | 标准打印  |
| 3     | 3×1  | **旋转90°** | 小尺寸卡片 |
| 4     | 2×2  | 不旋转       | 紧凑打印  |

## 🔧 配置文件

项目支持通过根目录下的 `config.yml` 文件覆盖默认配置。所有配置项均为可选，未配置的项将使用默认值。

### 配置文件位置

```
character-card/config.yml
```

### 配置项说明

配置项使用**小写驼峰**命名格式，与常量名一一对应：

| 配置项（小写驼峰）                     | 对应常量                             | 类型    | 默认值               |
| ----------------------------- | -------------------------------- | ----- | ----------------- |
| `cardAspectRatioHeightScale`  | `CARD_ASPECT_RATIO_HEIGHT_SCALE` | float | 4/3               |
| `colorBackground`             | `COLOR_BACKGROUND`               | str   | "#FFFFFF"         |
| `colorBorder`                 | `COLOR_BORDER`                   | str   | "#E0E0E0"         |
| `colorDivider`                | `COLOR_DIVIDER`                  | str   | "#E0E0E0"         |
| `colorMainPinyin`             | `COLOR_MAIN_PINYIN`              | str   | "#4A4A4A"         |
| `colorMainCharacter`          | `COLOR_MAIN_CHARACTER`           | str   | "#1A1A1A"         |
| `colorPhrasePinyin`           | `COLOR_PHRASE_PINYIN`            | str   | "#767676"         |
| `colorPhraseText`             | `COLOR_PHRASE_TEXT`              | str   | "#2B2B2B"         |
| `pixelsOuterMargin`           | `PIXELS_OUTER_MARGIN`            | int   | 20                |
| `pixelsBorderWidth`           | `PIXELS_BORDER_WIDTH`            | int   | 6                 |
| `pixelsDividerWidth`          | `PIXELS_DIVIDER_WIDTH`           | int   | 2                 |
| `pixelsDividerPadding`        | `PIXELS_DIVIDER_PADDING`         | int   | 40                |
| `ratioFontSizeMainCharacter`  | `RATIO_FONT_SIZE_MAIN_CHARACTER` | float | 0.6               |
| `ratioFontSizeMainPinyin`     | `RATIO_FONT_SIZE_MAIN_PINYIN`    | float | 0.12              |
| `ratioFontSizePhraseText`     | `RATIO_FONT_SIZE_PHRASE_TEXT`    | float | 0.12              |
| `ratioFontSizePhrasePinyin`   | `RATIO_FONT_SIZE_PHRASE_PINYIN`  | float | 0.035             |
| `ratioPosMainPinyinY`         | `RATIO_POS_MAIN_PINYIN_Y`        | float | 0.12              |
| `ratioPosMainGapY`            | `RATIO_POS_MAIN_GAP_Y`           | float | 0.05              |
| `ratioPosBottomAreaY`         | `RATIO_POS_BOTTOM_AREA_Y`        | float | 0.8               |
| `ratioPosPhrasePinyinY`       | `RATIO_POS_PHRASE_PINYIN_Y`      | float | 0.03              |
| `ratioPosPhraseGapY`          | `RATIO_POS_PHRASE_GAP_Y`         | float | 0.01              |
| `coefficientGridCenterWeight` | `COEFFICIENT_GRID_CENTER_WEIGHT` | float | 0.5               |
| `ratioCharSpacingOfWidth`     | `RATIO_CHAR_SPACING_OF_WIDTH`    | float | 0.1               |
| `characterFont`               | `CHARACTER_FONT`                 | str   | "fonts/FZKTK.TTF" |
| `pinyinFont`                  | `PINYIN_FONT`                    | str   | "fonts/msyh.ttc"  |
| `defaultCardWidth`            | `DEFAULT_CARD_WIDTH`             | int   | 1200              |
| `pdfMarginX`                  | `PDF_MARGIN_X`                   | int   | 30                |
| `pdfMarginY`                  | `PDF_MARGIN_Y`                   | int   | 40                |
| `cardImageAspectRatio`        | `CARD_IMAGE_ASPECT_RATIO`        | float | 0.75              |
| `cardGridScaleFactor`         | `CARD_GRID_SCALE_FACTOR`         | float | 0.95              |
| `colorTrimLine`               | `COLOR_TRIM_LINE`                | str   | "#D0D0D0"         |
| `widthTrimLine`               | `WIDTH_TRIM_LINE`                | float | 0.5               |
| `dashPatternTrimLine`         | `DASH_PATTERN_TRIM_LINE`         | list  | \[4.0, 4.0]       |
| `defaultImageNumsPerPage`     | `DEFAULT_IMAGE_NUMS_PER_PAGE`    | int   | 2                 |
| `rotationAngleDegrees`        | `ROTATION_ANGLE_DEGREES`         | int   | -90               |

### 配置示例

```yaml
# 修改卡片宽度和背景颜色
defaultCardWidth: 1500
colorBackground: "#FFF8E1"
colorMainCharacter: "#000000"

# 修改每页默认卡片数
defaultImageNumsPerPage: 4
```

### 配置优先级

1. `config.yml` 文件中的配置（如果存在）
2. `const/__init__.py` 中的默认常量值

## 🔄 数据流

```
用户配置（CLI/CSV）
        ↓
ChineseCharacterConfig（config/character.py）
        ↓
draw_single_card() → PNG 图片（util/card_maker.py）
        ↓
export_images_to_pdf() → PDF 文件（util/pdf_maker.py）
```

## 📝 使用示例

### 完整工作流

1. **创建 CSV 配置文件** `config.csv`：

```csv
character,character_pinyin,phrases,phrases_pinyin
天,tian1,天空|天堂,tian1 kong1|tian1 tang2
地,di4,大地|地球,da4 di4|di4 qiu2
人,ren2,人们|人类,ren2 men|ren2 lei4
```

1. **生成卡片图片**：

```bash
python main.py card generate --config config.csv -o ./cards
```

1. **导出 PDF**：

```bash
python main.py pdf export -i ./cards -o ./cards.pdf -n 4
```

## 📄 卡片布局

```
┌─────────────────────────────┐
│     zhōng guó               │  ← 主汉字拼音
│                             │
│           中                │  ← 大字号主汉字
│                             │
│─────────────────────────────│
│                             │
│    tiān kōng     tiān táng  │  ← 词组拼音（按词组分组）
│      天空           天堂     │  ← 常用词组（横向排列）
│                             │
└─────────────────────────────┘
```

**布局说明**：

- 顶部：主汉字拼音（支持多音字）
- 中心：大字号主汉字
- 底部：常用词组（最多3个），每个词组的拼音在汉字上方，词组之间横向均匀分布

## 📦 构建打包

### 环境要求

- **Python**: ≥3.12
- **包管理器**: uv
- **打包工具**: PyInstaller（将由打包脚本自动安装）

### Linux / macOS

使用一键打包脚本：

```bash
./scripts/build.sh
```

脚本执行步骤：

1. 安装项目依赖（`uv sync`）
2. 安装 PyInstaller
3. 执行打包（`pyinstaller character-card.spec`）
4. 复制配置文件到输出目录

### Windows

在 Windows 环境下，按以下步骤手动打包：

```powershell
# 1. 安装项目依赖
uv sync

# 2. 安装 PyInstaller
uv pip install pyinstaller

# 3. 执行打包
uv run pyinstaller character-card.spec

# 4. 复制配置文件到输出目录
copy config.yml dist\
```

### 输出文件

打包完成后，输出目录结构如下：

```
dist/
├── character-card      # Linux/macOS 可执行文件
├── character-card.exe  # Windows 可执行文件（Windows 环境下生成）
└── config.yml          # 配置文件（可手动修改）
```

### 使用可执行文件

# 进入输出目录

```
cd dist
```
<br />

# 查看帮助

```
./character-card --help
```
<br />

# 生成卡片

```
./character-card card generate -c 天:tian1
```

<br />

# 导出 PDF

```

./character-card pdf export -i ./output/images -o ./cards.pdf
```

### 配置文件覆盖

打包后的可执行文件支持配置文件覆盖：

1. **内置配置**：可执行文件内部已包含默认配置
2. **外部配置**：在可执行文件同目录下放置 `config.yml`，将优先使用外部配置

这样用户可以在不修改源码的情况下自定义卡片样式和布局。

## 🧪 测试

项目使用 `pytest` 进行单元测试和集成测试，覆盖核心功能模块。

### 安装测试依赖

```bash
uv pip install -e ".[dev]"
```

### 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest test/test_card_cli.py

# 显示详细输出
pytest -v
```

### 测试覆盖范围

| 测试文件 | 测试类型 | 覆盖内容 |
|---------|---------|---------|
| `test_character.py` | 单元测试 | 汉字配置解析、拼音校验、词组解析 |
| `test_csv.py` | 单元测试 | CSV 加载逻辑、路径校验、行范围截取 |
| `test_card_cli.py` | 集成测试 | card 子命令参数解析、文件生成流程 |
| `test_pdf_cli.py` | 集成测试 | pdf 子命令参数解析、PDF 导出流程 |

### 测试目录结构

```
test/
├── conftest.py          # pytest 配置和全局 fixtures
├── fixtures/            # 测试资源文件
│   └── test_config.csv  # 测试用 CSV 配置文件
├── test_character.py    # 汉字配置解析单元测试
├── test_csv.py          # CSV 加载逻辑单元测试
├── test_card_cli.py     # card 子命令集成测试
└── test_pdf_cli.py      # pdf 子命令集成测试
```

## 📜 许可证

MIT License
