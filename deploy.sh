#!/bin/bash

# Hexo 博客快速部署脚本
# 使用: ./deploy.sh "提交信息" 或 ./deploy.sh

set -e

COMMIT_MSG="${1:-(Site updated: $(date '+%Y-%m-%d %H:%M:%S'))}"

echo "🚀 开始部署 Hexo 博客..."
echo "📝 提交信息: $COMMIT_MSG"

# 1. 清理旧文件
echo "🧹 清理旧文件..."
npm run clean

# 2. 生成静态网站
echo "🏗️  生成新网站..."
npm run build

# 3. 提交源代码到 source 分支
echo "📦 提交源代码..."
git add .
git commit -m "$COMMIT_MSG" || echo "⏭️  没有新更改"
git push origin source || echo "⚠️  source 分支推送失败"

# 4. 部署到 GitHub Pages (main 分支)
echo "🚢 部署到 GitHub Pages..."
npm run deploy

echo ""
echo "✅ 部署完成！"
echo "🌐 访问你的博客: https://infinitepwn.github.io"
echo "📝 GitHub 仓库: https://github.com/infinitepwn/infinitepwn.github.io"
