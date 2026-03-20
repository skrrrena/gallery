#!/bin/zsh
# 一键发布：更新所有图片列表 → commit → push
#
# 用法：
#   ./publish.sh                      → commit message: "update"
#   ./publish.sh "add new photos"     → 自定义 commit message
#
# 添加图片的工作流：
#   把图片放进对应的 assets/sN-xxx/ 文件夹，然后运行 ./publish.sh
#   脚本会自动扫描所有文件夹并更新 list.json，不需要手动维护
#
# 前提：已在项目目录下执行过 git remote add origin <your-repo>

MSG=${1:-"update"}

echo "→ 更新所有图片列表..."
node update-cover-list.js
node update-ceramics-list.js
node update-vermilion-list.js
node update-amber-list.js
node update-portraiture-list.js

echo "→ 暂存所有变更..."
git add -A

# 检查是否有东西可提交
if git diff --cached --quiet; then
  echo "✓ 没有变更，无需提交"
  exit 0
fi

echo "→ 提交：$MSG"
git commit -m "$MSG"

echo "→ 推送到 GitHub..."
git push

echo "✓ 完成！网站约 30 秒后更新"
