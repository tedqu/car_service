#!/bin/bash

# 停止并移除已存在的 Docker 容器
echo "Stopping existing Docker containers..."
docker-compose down

# 构建 Docker 镜像
echo "Building Docker images..."
docker-compose build

# 启动 Docker 容器
echo "Starting Docker containers..."
docker-compose up -d mysql-car \
&& sleep 5
docker-compose up -d main-car

# 显示容器状态
echo "Docker containers are up and running."
docker ps

