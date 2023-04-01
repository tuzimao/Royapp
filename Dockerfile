# 使用官方 Python 基础镜像
FROM python:3.9

# 安装Node.js和npm
RUN curl -sL https://deb.nodesource.com/setup_14.x | bash -
RUN apt-get install -y nodejs

# 更新并安装一些基本的系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 将工作目录设置为 /app
WORKDIR /app

# 将 Flask 后端代码复制到工作目录
COPY backend/requirements.txt .

# 安装 Python 依赖库
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# 复制后端应用程序代码
COPY backend/ .

# 进入前端项目目录
WORKDIR /app/frontend

# 复制前端应用程序代码
COPY frontend/ .

# 安装前端依赖库并构建生产版本
RUN npm install
RUN npm run build

# 将构建产物复制到 Flask 静态文件夹
WORKDIR /app
RUN mkdir -p static
RUN cp -r frontend/dist/* static/

# 设置容器中的环境变量
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# 暴露后端服务器端口
EXPOSE 5000

# 运行 Flask 服务器
CMD ["flask", "run"]
