from pathlib import Path
from typing import Generator, Optional
import polars as pl

# 假设您已引入或定义了相关的依赖
# from your_module import ChineseCharacterConfig, CharacterConfigException
from config.character import ChineseCharacterConfig

def load_configs_from_csv(
    csv_path: Path, 
    start_row: Optional[int] = None, 
    end_row: Optional[int] = None
) -> Generator[ChineseCharacterConfig, None, None]:
    """
    🚀 利用 Polars 引擎多线程并发流式解析几千行 CSV 配置文件。
    支持通过 start_row 和 end_row 截取指定范围的行数据。
    """
    # 1. 🔑 【深度路径校验】：细致校验路径类型与存在状态
    if not csv_path.exists():
        raise FileNotFoundError(f"错误: 未找到指定的 CSV 配置文件: {csv_path}")
        
    if csv_path.is_dir():
        # 如果传入的是目录而不是具体文件，抛出针对性的标准异常
        raise IsADirectoryError(
            f"错误: 目标路径 '{csv_path}' 是一个目录（文件夹）。"
            f"请指定具体的 CSV 配置文件完整路径（包含文件名与后缀）。"
        )

    # 2. 【校验规则 1】：要么都为 None，要么都不为 None
    if (start_row is None) != (end_row is None):
        raise ValueError("参数错误: start_row 和 end_row 必须同时为 None，或同时提供整数值。")

    try:
        # Polars 的 read_csv 基于 Rust 实现，自动处理多线程并完美兼容带有 BOM 的 UTF-8 文件
        df = pl.read_csv(csv_path, low_memory=True)
    except Exception as e:
        raise Exception(f"CSV 文件加载失败，可能编码不正确或文件损坏。原因: {e}")

    # 校验 CSV 核心表头是否完备
    required_columns = {"character", "character_pinyin", "phrases", "phrases_pinyin"}
    if not required_columns.issubset(set(df.columns)):
        raise Exception(f"CSV 格式不合法。表头必须完整包含: {required_columns}")

    # 3. 如果提供了行数范围，则执行切片逻辑
    if start_row is not None and end_row is not None:
        # 【校验规则 2】：当 start_row > end_row 时，交换他俩
        if start_row > end_row:
            start_row, end_row = end_row, start_row
            
        start_index = max(0, start_row - 1)
        end_index = end_row
        
        # 利用 Polars 高性能切片直接截取 DataFrame，避免多余行的迭代开销
        df = df[start_index:end_index]

    # 4. iter_rows(named=True) 会将切片后的行高效地转为 Python 的 dict 结构
    for row_dict in df.iter_rows(named=True):
        # 过滤掉主汉字完全为空的无效干扰行
        char_val = row_dict.get("character")
        if char_val is None or str(char_val).strip() == "":
            continue
            
        # 流式返回实例化对象
        yield ChineseCharacterConfig.from_csv_row(row_dict)
    