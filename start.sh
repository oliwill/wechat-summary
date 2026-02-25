#!/bin/bash

# 启动脚本

echo "========================================="
echo "微信群讨论总结工具 - 启动"
echo "========================================="
echo ""

# 检查 Python 版本
python3 --version

# 检查依赖
echo "检查依赖..."
pip install -r requirements.txt

# 检查配置文件
if [ ! -f ".env" ]; then
    echo "⚠️  配置文件不存在，使用测试配置..."
    cp .env.test .env
fi

# 运行测试
echo ""
echo "运行测试..."
python3 test.py

# 询问是否运行主程序
echo ""
read -p "是否运行主程序？(y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "启动主程序..."
    python3 main.py
fi
