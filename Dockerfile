# 使用官方 Python 基础镜像
FROM python:3.12-slim

# 设置时区
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone


# 设置工作目录
WORKDIR /app

# 安装系统编译依赖（解决 reportlab 编译问题）
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libfreetype6-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# 先复制依赖文件
COPY requirements.txt .
RUN pip install --upgrade pip
# 安装 Python 依赖（自动使用上述镜像源）
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 暴露端口
EXPOSE 5000

# 生产环境启动命令
CMD ["gunicorn", \
    "--bind", "0.0.0.0:5000", \
    "--workers", "2", \
    "--threads", "2", \
    "app:create_app()"]