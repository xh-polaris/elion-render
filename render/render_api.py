import base64
import logging
import zlib
from io import BytesIO

from flask import Blueprint, request

from common import rex
from common.errorx import BizException
from evaluate.micro_builder import MicroEvaluationBuilder
from common.util import png2pdf, nc_param
from render.render_core import Render

bp = Blueprint("render", __name__)


@bp.post("/render")
def render():
    # 批改
    try:
        data = request.get_json()
        suffix = nc_param(data, "suffix")
        r = Render(nc_param(data, "title"), nc_param(data, "content"),
                   MicroEvaluationBuilder.build(nc_param(data, "raw")))

        # 分页
        result = r.paging().imgs if nc_param(data, "paging") else [r.img]
        # 格式转换
        result = (
            [png2pdf(result)]  # PDF 情况：返回单元素列表（PDF bytes）
            if suffix == "pdf"
            else [
                (buf := BytesIO(), img.save(buf, format="PNG"), buf.getvalue())[2]  # PNG 情况：每张图转 bytes
                for img in result
            ]
        )
        # 编码（先压缩再 Base64）
        result = [base64.b64encode(zlib.compress(data)).decode("utf-8") for data in result]

        return rex.succeed({
            "suffix": suffix,
            "result": result,
            "compressed": True  # 告诉前端数据是压缩过的
        })
    except BizException as e:
        return rex.fail(e)
    except Exception as e:
        logging.error(f"渲染失败, 原因{e}")
        return rex.fail(str(e), 999, "渲染失败")
