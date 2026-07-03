import typer
from typing import Annotated
from pathlib import Path
from util.pdf_maker import export_images_to_pdf
from util.path_safety import safe_resolve_path
from rich.console import Console
import const

app = typer.Typer(name="pdf", help="PDF 导出自命令")
console = Console()


def _process_output_path(output_path: Path) -> Path:
    """
    业务逻辑：处理并验证导出的 PDF 路径。

    1. 检查是否为目录，如果是则拦截抛出 typer.BadParameter 异常。
    2. 检查是否为 .pdf 后缀，如果不是则拦截抛出 typer.BadParameter 异常。
    3. 如果合规，确保该文件所在的所有上级父目录、中间目录全部安全存在。
    """
    resolved_path = safe_resolve_path(output_path)

    if resolved_path.is_dir():
        raise typer.BadParameter(
            f"目标路径 '{output_path}' 是一个目录。请指定具体的 PDF 完整文件路径（包含文件名）。"
        )

    if resolved_path.suffix.lower() != ".pdf":
        raise typer.BadParameter(
            f"非法的目标格式 '{output_path}'。请确保文件路径以 '.pdf' 后缀结尾。"
        )

    resolved_path.parent.mkdir(parents=True, exist_ok=True)

    return resolved_path


@app.command(help="将卡片图片导出为 PDF")
def export(
    image_path: Annotated[
        Path, typer.Option("--images", "-i", help="PNG 图片目录路径（必填）")
    ],
    output_path: Annotated[
        Path,
        typer.Option(
            "--output", "-o", help="PDF 文件输出路径（必填），必须以 .pdf 结尾"
        ),
    ],
    nums_per_page: Annotated[
        int | None,
        typer.Option("--nums", "-n", help="每页卡片数，支持 1/2/3/4，默认 2"),
    ] = None,
):
    try:
        console.print(
            f"[bold][green]要读取图片的路径是:[red]{image_path}[red][green][bold]"
        )

        resolved_output_path = _process_output_path(output_path)
        console.print(
            f"[bold][green]输出的pdf文件是:[red]{resolved_output_path}[red][green][bold]"
        )
        nums_per_page = nums_per_page or const.DEFAULT_IMAGE_NUMS_PER_PAGE
        console.print(
            f"[bold][green]每页输出:[red]{nums_per_page}[red]张图片[green][bold]"
        )

        export_images_to_pdf(image_path, str(resolved_output_path), n=nums_per_page)

        console.print(
            f"[bold][cyan]导出完成,生成的pdf文件是: [red]{resolved_output_path}[red][cyan][bold]"
        )
    except typer.Exit:
        raise
    except Exception as e:
        console.print(f"[bold][red]错误: {e}[red][bold]")
        raise typer.Exit(code=1)
