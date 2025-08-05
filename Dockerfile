# 使用轻量 Python 镜像
FROM python:3.8-slim

# 设置工作目录
WORKDIR /app

# 安装系统级依赖（支持 bcrypt 编译）
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# 安装 Python 依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制代码
COPY . .

# 运行 Flask 应用
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]
