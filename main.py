import typer

from subcommand.card import app as card_app
from subcommand.pdf import app as pdf_app 

app = typer.Typer(
    name="character-card",
    help="汉字卡片生成工具 - 快速生成汉字学习卡片图片并导出为 PDF"
)

app.add_typer(card_app, name="card", help="生成汉字卡片图片")
app.add_typer(pdf_app, name="pdf", help="将卡片图片导出为 PDF")


if __name__ == "__main__":
    app()