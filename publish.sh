#!/bin/zsh
# 一键发布：更新图片列表 → commit → push
#
# 用法：
#   ./publish.sh                      → commit message: "update"
#   ./publish.sh "add new ceramics"   → 自定义 commit message
#
# 修改内容的方式：
#   图片（封面轮播）：把图放进 assets/cover/         → 运行 ./publish.sh
#   图片（陶瓷页）：  把图放进 assets/ceramics/（或命名为 ceramics-xx 放在 assets/）
#                    然后运行 ./publish.sh
#   文字/联系方式：   编辑 content.json                 → 运行 ./publish.sh
#
# 前提：已在项目目录下执行过 git remote add origin <your-repo>

MSG=${1:-"update"}

echo "→ 更新图片列表..."
python3 update-cover-list.py
python3 update-ceramics-list.py

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
