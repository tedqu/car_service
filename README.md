# Temp Name

Flask 应用，后端服务器，数据库存储，测试单元

## 开始

以下指南将帮助您在本地机器上为开发和测试目的设置和运行这个项目。

### 先决条件

在开始之前，需要安装以下软件：

- Python 3.8+
- Docker
- Docker Compose

### 安装

按照以下步骤设置您的本地开发环境：

1. **克隆仓库**

   ```bash
   git clone git@github.com:tedqu/car_service.git
   cd car_service

2. **配置环境变量复制 .env.example 文件为 .env，并根据需要更新环境变量：**
   ```bash
   cp .env.example .env

3. **启动**
   ```bash
   bash start.sh

4. **测试代码**
   ```bash
   python3 -m unittest tests/test_routes.py
