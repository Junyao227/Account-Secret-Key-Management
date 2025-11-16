FROM python:3.11-slim

WORKDIR /app

# 先装依赖（使用国内镜像源，避免访问 files.pythonhosted.org 超时）
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

# 拷贝代码
COPY . .

# 使用环境变量里的 DATABASE_URL（docker-compose 里会设置）
ENV DATABASE_URL=postgresql://user:password@db:5432/windsurf_pool

# 启动 FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
