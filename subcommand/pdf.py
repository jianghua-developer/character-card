import typer
from typing import Annotated
from pathlib import Path
from util.pdf_maker import export_images_to_pdf
from rich.console import Console
import const

app = typer.Typer(name="pdf", help="PDF 导出自命令")
console = Console()


def _process_output_path(output_path: Path):
    """
    业务逻辑：处理并验证导出的 PDF 路径。

    1. 检查是否为目录，如果是则拦截抛出 typer.BadParameter 异常。
    2. 检查是否为 .pdf 后缀，如果不是则拦截抛出 typer.BadParameter 异常。
    3. 如果合规，确保该文件所在的所有上级父目录、中间目录全部安全存在。
    """
    # 1. 检查路径是否明确指向一个已存在的目录
    if output_path.is_dir():
        raise typer.BadParameter(
            f"目标路径 '{output_path}' 是一个目录。请指定具体的 PDF 完整文件路径（包含文件名）。"
        )

    # 2. 检查文件后缀是否为标准的小写 .pdf
    # output_path.suffix 可以拿到形如 ".pdf" 的后缀，.lower() 确保对 .PDF 或 .Pdf 同样兼容
    if output_path.suffix.lower() != ".pdf":
        raise typer.BadParameter(
            f"非法的目标格式 '{output_path}'。请确保文件路径以 '.pdf' 后缀结尾。"
        )

    # 3. 如果路径合规，提取其所在的父级文件夹，并确保所有上级/中间目录 100% 存在
    # parents=True 表示递归创建所有中间目录，exist_ok=True 表示若目录已存在则静默跳过不报错
    output_path.parent.mkdir(parents=True, exist_ok=True)


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
    console.print(
        f"[bold][green]要读取图片的路径是:[red]{image_path}[red][green][bold]"
    )

    _process_output_path(output_path)
    console.print(f"[bold][green]输出的pdf文件是:[red]{output_path}[red][green][bold]")
    nums_per_page = nums_per_page or const.DEFAULT_IMAGE_NUMS_PER_PAGE
    console.print(f"[bold][green]每页输出:[red]{nums_per_page}[red]张图片[green][bold]")

    try:
        export_images_to_pdf(image_path, str(output_path), n=nums_per_page)
    except Exception as e:
        raise typer.BadParameter(str(e))

    console.print(
        f"[bold][cyan]导出完成,生成的pdf文件是: [red]{output_path}[red][cyan][bold]"
    )
