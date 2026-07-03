#!/bin/bash
set -e

echo "=== character-card 打包脚本 ==="

echo ""
echo "1. 安装依赖..."
uv sync

echo ""
echo "2. 安装 PyInstaller..."
uv pip install pyinstaller

echo ""
echo "3. 开始打包..."
uv run pyinstaller character-card.spec

echo ""
echo "4. 复制配置文件到输出目录..."
cp config.yml dist/

echo ""
echo "=== 打包完成 ==="
echo "输出文件: dist/character-card"
echo "配置文件: dist/config.yml"
