import typer
import const
from typing import Annotated, Generator
from rich.console import Console
from rich.table import Table
from config.character import (
    ChineseCharacterConfig,
    ChineseCharacterPhraseConfig,
    check_pinyin_invalid,
)
from util.card_maker import draw_single_card
from util.csv import load_configs_from_csv
from util.path_safety import safe_resolve_path
from pathlib import Path


app = typer.Typer(name="card", help="汉字卡片生成子命令")

console = Console()


def _check_pinyin_invalid(pinyin_strs: list[str]):
    try:
        check_pinyin_invalid(pinyin_strs)
    except Exception as e:
        raise typer.BadParameter(str(e))


def _process_character_pinyin(character_pinyin: str) -> list[str] | None:
    result: list[str] | None = None
    if character_pinyin:
        result = character_pinyin.split(",")
        _check_pinyin_invalid(result)

    return result


def _process_character_phrases(character_phrases: str):
    result: list[ChineseCharacterPhraseConfig] | None = None
    if character_phrases:
        result = []
        character_phrases_strs = character_phrases.split(",")
        if len(character_phrases_strs) > 3:
            raise typer.BadParameter(f"最多配置三个词语:{character_phrases}")
        for s in character_phrases_strs:
            try:
                result.append(ChineseCharacterPhraseConfig.from_str(s))
            except Exception as e:
                raise typer.BadParameter(str(e))
    return result


def _parse_chinese_character_config(value: str) -> ChineseCharacterConfig:
    configs = value.split(":")
    if len(configs) == 1:
        character = configs[0]
        return ChineseCharacterConfig(character)

    if len(configs) == 2:
        character, character_pinyin = configs
        return ChineseCharacterConfig(
            character, character_pinyin=_process_character_pinyin(character_pinyin)
        )

    if len(configs) == 3:
        character, character_pinyin, character_phrases = configs

        return ChineseCharacterConfig(
            character,
            character_pinyin=_process_character_pinyin(character_pinyin),
            character_phrases=_process_character_phrases(character_phrases),
        )

    raise typer.BadParameter(
        f"invalid character config:{value}格式不正确；示例：天:tian1:天空@tian1#kong1,天堂@tian1#tang2"
    )


def _print_chinese_character_config(
    chinese_character_configs: list[ChineseCharacterConfig],
):
    table = Table("character", "phrases", "computed_pinyin")

    console.print("[bold][green]汉字参数:[green][bold]")

    for config in chinese_character_configs:
        table.add_row(
            config.character,
            str(config.character_phrases),
            str(config.computed_character_pinyin),
        )

    console.print(table)


def _process_output_path(
    output_path: Annotated[Path | None, typer.Option("--output", "-o")] = None,
) -> Path | None:
    if output_path:
        resolved_path = safe_resolve_path(output_path)

        if resolved_path.exists() and not resolved_path.is_dir():
            raise typer.BadParameter(f"输出目录不能配置为文件:{output_path}")

        resolved_path.mkdir(parents=True, exist_ok=True)

        return resolved_path

    return output_path


def _generate_image(
    chinese_character_configs: list[ChineseCharacterConfig]
    | Generator[ChineseCharacterConfig, None, None],
    width: int | None = None,
    output_path: Path | None = None,
):

    output_path = _process_output_path(output_path)
    console.print(f"[bold][green]图片的保存目录为:[red]{output_path}[red][green][bold]")
    console.print("[bold][green]正在生成图片...[green][bold]")
    for config in chinese_character_configs:
        path = draw_single_card(
            config, width=width or const.DEFAULT_CARD_WIDTH, output_path=output_path
        )
        console.print(
            f"[bold][cyan]图片[cyan] [red]{path}[red] [cyan]已生成[cyan][bold]"
        )


def _process_chinese_character_configs(
    chinese_character_configs: list[ChineseCharacterConfig],
    width: int | None = None,
    output_path: Path | None = None,
):
    _print_chinese_character_config(chinese_character_configs)

    config_correct = typer.confirm("拼音配置是否正确？", abort=True)

    if config_correct:
        _generate_image(chinese_character_configs, width=width, output_path=output_path)


def _process_config_file(
    config_file: Path,
    start_row: int | None = None,
    end_row: int | None = None,
    width: int | None = None,
    output_path: Path | None = None,
):

    _generate_image(
        load_configs_from_csv(config_file, start_row=start_row, end_row=end_row),
        width=width,
        output_path=output_path,
    )


@app.command(help="生成汉字卡片图片")
def generate(
    chinese_character_configs: Annotated[
        list[ChineseCharacterConfig],
        typer.Option(
            "--character",
            "-c",
            parser=_parse_chinese_character_config,
            help="汉字配置，格式：汉字:拼音1,拼音2:词组1@拼音#拼音,词组2@拼音#拼音；示例：天:tian1:天空@tian1#kong1,天堂@tian1#tang2",
        ),
    ] = [],
    output_path: Annotated[
        Path | None,
        typer.Option(
            "--output",
            "-o",
            resolve_path=True,
            help="图片输出目录，默认 output/images/",
        ),
    ] = None,
    width: Annotated[
        int | None, typer.Option("--width", "-w", help="卡片宽度（像素），默认 1200")
    ] = None,
    config_file: Annotated[
        Path | None,
        typer.Option(
            "--config", resolve_path=True, help="CSV 配置文件路径，与 --character 互斥"
        ),
    ] = None,
    start_row: Annotated[
        int | None, typer.Option("--start", help="CSV 起始行（配合 --config 使用）")
    ] = None,
    end_row: Annotated[
        int | None, typer.Option("--end", help="CSV 结束行（配合 --config 使用）")
    ] = None,
):
    try:
        if not chinese_character_configs and config_file is None:
            console.print("没有找到配置，退出...")
            raise typer.Exit()

        if chinese_character_configs and config_file is not None:
            raise typer.BadParameter("--character 和 --config 不能同时配置")

        if config_file is not None:
            _process_config_file(
                config_file,
                start_row=start_row,
                end_row=end_row,
                width=width,
                output_path=output_path,
            )
        else:
            _process_chinese_character_configs(
                chinese_character_configs, width=width, output_path=output_path
            )
    except typer.Exit:
        raise
    except typer.BadParameter:
        raise
    except Exception as e:
        console.print(f"[bold][red]错误: {e}[red][bold]")
        raise typer.Exit(code=1)
