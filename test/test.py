import base64
import json
import zlib
import io
import os
import tempfile
from PIL import Image
import subprocess
import re


def decode_and_display(base64_str):
    try:
        # 解码 Base64
        decoded_data = base64.b64decode(base64_str)

        # 尝试解压（如果是压缩过的数据）
        try:
            decompressed_data = zlib.decompress(decoded_data)
            decoded_data = decompressed_data
            print("检测到数据经过 zlib 压缩，已解压")
        except zlib.error:
            pass  # 不是压缩数据

        # 检测文件类型
        if decoded_data.startswith(b'\x89PNG'):
            # 显示 PNG 图片
            img = Image.open(io.BytesIO(decoded_data))
            img.show()
            print("显示 PNG 图片")
        elif decoded_data.startswith(b'%PDF'):
            # 保存并打开 PDF 文件
            with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
                tmp.write(decoded_data)
                tmp_path = tmp.name

            # 根据不同平台打开 PDF
            if os.name == 'nt':  # Windows
                os.startfile(tmp_path)
            elif os.name == 'posix':  # Linux/macOS
                opener = "open" if sys.platform == "darwin" else "xdg-open"
                subprocess.run([opener, tmp_path])
            print(f"PDF 文件已保存到临时路径: {tmp_path}")
        else:
            print("未知文件格式，已解码为原始数据")
            print(f"前 32 字节: {decoded_data[:32]}")

    except Exception as e:
        print(f"解码失败: {e}")


def read_base64_from_file(content):
    try:
        content = content.strip()
        # 移除可能的 data URI 前缀（如 "data:image/png;base64,"）
        if ";base64," in content:
            content = content.split(";base64,")[1]

        # 移除所有非 Base64 字符（如换行符、空格）
        base64_str = re.sub(r"[^a-zA-Z0-9+/=]", "", content)

        if base64_str:
            decode_and_display(base64_str)
        else:
            print("文件内容为空或无效")
    except Exception as e:
        print(f"读取文件失败: {e}")


if __name__ == "__main__":
    file_path = "test.json"
    with open(file_path, 'r', encoding='utf-8') as f:
        json_data = json.load(f)  # 正确：json.load() 从文件对象解析
        for img in json_data["payload"]["result"]:
            read_base64_from_file(img)
