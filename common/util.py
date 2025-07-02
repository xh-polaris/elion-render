from io import BytesIO
from typing import Any

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader

from common.errorx import BizException


def png2pdf(images):
    """
    将多个 PIL Image 对象合并成一个 PDF，返回 PDF 的 bytes 数据

    Args:
        images (List[PIL.Image]): 要合并的 PIL Image 列表

    Returns:
        bytes: PDF 文件的二进制数据
    """
    buffer = BytesIO()  # 用于存储 PDF 的缓冲区

    # 创建 PDF 画布
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter  # PDF 页面尺寸（默认 A4）

    for img in images:
        # 调整图片大小以适应 PDF 页面
        img_width, img_height = img.size
        scale = min(width / img_width, height / img_height)
        img_width *= scale
        img_height *= scale

        # 在 PDF 上绘制图片
        c.drawImage(ImageReader(img), 0, 0, width=img_width, height=img_height)
        c.showPage()  # 结束当前页

    c.save()  # 保存 PDF
    pdf_bytes = buffer.getvalue()
    buffer.close()

    return pdf_bytes


def nc_param(data: dict[str, Any], key: str):
    if key not in data:
        raise BizException(1000, f"参数{key}不存在")
    return data[key]
