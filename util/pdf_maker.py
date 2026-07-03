from pathlib import Path
from reportlab.pdfgen import canvas
import const

from reportlab.lib.pagesizes import A4

        # 顺时针旋转 90 度 (ReportLab 中负数代表顺时针)


# ==================== 职责单一化拆分函数 ====================

def _collect_png_images(image_dir: Path) -> list[str]:
    """职责 1: 负责目录的合法性校验与 PNG 图片路径收集"""
    if not image_dir.is_dir():
        raise NotADirectoryError(f"错误: 传入的路径 '{image_dir}' 不是一个合法或已存在的目录。")
        
    image_paths = [str(p) for p in image_dir.glob("*.png")]
    
    if not image_paths:
        raise FileNotFoundError(f"错误: 在目录 '{image_dir}' 下未找到任何 PNG 图片，无法生成 PDF。")
        
    return image_paths


def _calculate_card_dimensions(n: int) -> tuple[int, int, float, float, bool]:
    """职责 2: 负责根据页面尺寸和网格数，计算每张卡片最终的渲染宽高、网格行列数以及是否需要旋转"""
    VALID_NUMS = (1, 2, 3, 4)
    ROTATED_NUMS = (2, 3)

    if n not in VALID_NUMS:
        raise ValueError("参数错误: 每页卡片张数 n 目前仅支持设置为 1, 2, 3, 4。")

    a4_w, a4_h = const.PDF_PAGE_SIZE
    rows, cols = const.GRID_LAYOUT_MAP.get(n, const.DEFAULT_GRID_LAYOUT)
    
    # 动态决策布局网格与旋转策略
    is_rotated = True if n in ROTATED_NUMS else False

    # 计算单个网格单元格的可用宽高
    cell_w = (a4_w - const.PDF_MARGIN_X * 2) / cols
    cell_h = (a4_h - const.PDF_MARGIN_Y * 2) / rows
    
    # 依据是否旋转，决定对齐的宽高比目标
    target_aspect_ratio = 1 / const.CARD_IMAGE_ASPECT_RATIO if is_rotated else const.CARD_IMAGE_ASPECT_RATIO

    if (cell_w / cell_h) > target_aspect_ratio:
        draw_h = cell_h * const.CARD_GRID_SCALE_FACTOR
        draw_w = draw_h * target_aspect_ratio
    else:
        draw_w = cell_w * const.CARD_GRID_SCALE_FACTOR
        draw_h = draw_w / target_aspect_ratio
        
    return rows, cols, draw_w, draw_h, is_rotated


def _calculate_grid_cell_origin(page_idx: int, cols: int, cell_w: float, cell_h: float) -> tuple[float, float]:
    """职责 3: 负责计算当前网格单元在标准 PDF 坐标系（左下角为原点）中的绝对起始 (x, y) 坐标"""
    a4_h = const.PDF_PAGE_SIZE[1]
    row_idx = page_idx // cols
    col_idx = page_idx % cols
    
    cell_x = const.PDF_MARGIN_X + col_idx * cell_w
    cell_y = a4_h - (const.PDF_MARGIN_Y + (row_idx + 1) * cell_h)
    return cell_x, cell_y


def _render_card_content(c: canvas.Canvas, img_path: str, cell_x: float, cell_y: float, cell_w: float, cell_h: float, draw_w: float, draw_h: float, is_rotated: bool):
    """职责 4: 负责处理网格内部的坐标变换（平移、旋转），并精确渲染卡片内容与裁剪虚线"""
    c.saveState()  # 隔离当前网格的画笔与坐标系状态
    
    if is_rotated:
        # 计算在物理网格内的居中偏移量
        offset_x = (cell_w - draw_w) / 2
        offset_y = (cell_h - draw_h) / 2
        
        # 将绘图原点平移到卡片在网格中居中摆放后的【左上角】坐标
        c.translate(cell_x + offset_x, cell_y + offset_y + draw_h)
        c.rotate(const.ROTATION_ANGLE_DEGREES)
        
        # 旋转后原宽变高，原高变宽映射给图像参数
        img_w, img_h = draw_h, draw_w
        render_x, render_y = 0.0, 0.0
    else:
        # 标准非旋转模式
        content_x = cell_x + (cell_w - draw_w) / 2
        content_y = cell_y + (cell_h - draw_h) / 2
        img_w, img_h = draw_w, draw_h
        render_x, render_y = content_x, content_y

    # 绘制字卡图片
    c.drawImage(img_path, render_x, render_y, width=img_w, height=img_h)
    
    # 绘制裁剪虚线框
    c.setStrokeColor(const.COLOR_TRIM_LINE)            
    c.setLineWidth(const.WIDTH_TRIM_LINE)              
    c.setDash(const.DASH_PATTERN_TRIM_LINE)            
    c.rect(render_x, render_y, img_w, img_h, stroke=1, fill=0) 
    
    c.restoreState()  # 恢复坐标系与画笔状态


# ==================== 主入口核心控制函数 ====================

def export_images_to_pdf(image_dir: Path, pdf_path: str, n: int = 4):
    """
    职责 5: 主控流水线，负责协调各个组件调度并控制 PDF 页面的生命周期。
    """
    image_paths = _collect_png_images(image_dir)
    rows, cols, draw_w, draw_h, is_rotated = _calculate_card_dimensions(n)
    
    c = canvas.Canvas(pdf_path, pagesize=const.PDF_PAGE_SIZE)
    a4_w, a4_h = const.PDF_PAGE_SIZE
    
    cell_w = (a4_w - const.PDF_MARGIN_X * 2) / cols
    cell_h = (a4_h - const.PDF_MARGIN_Y * 2) / rows
    total_images = len(image_paths)

    for i, img_path in enumerate(image_paths):
        page_idx = i % n
        
        # 1. 计算当前网格的物理原点坐标
        cell_x, cell_y = _calculate_grid_cell_origin(page_idx, cols, cell_w, cell_h)
        
        # 2. 渲染内容与裁剪线
        _render_card_content(c, img_path, cell_x, cell_y, cell_w, cell_h, draw_w, draw_h, is_rotated)
        
        # 3. 控制 PDF 换页逻辑
        if page_idx == n - 1 or i == total_images - 1:
            c.showPage()
            
    c.save()



if __name__ == "__main__":
    export_images_to_pdf(Path("/home/jeff/test/"), "/home/jeff/test/test.pdf", 4)
