#!/bin/zsh
# 一键发布：校验图片列表 → commit → push
#
# 用法：
#   ./publish.sh                      → commit message: "update"
#   ./publish.sh "add new photos"     → 自定义 commit message
#
# list.json 现在是仓库里的权威内容，不再由这个脚本自动生成/覆盖。
# 这里只做只读校验（不带 --import，update-all-lists.py 默认不写入任何
# 文件），提示磁盘和 list.json 之间的差异，方便你发现"忘了导入新图"或
# "有孤儿文件"之类的情况。如果要真正把新增/删除的文件写进 list.json，
# 手动运行 python3 update-all-lists.py --import。
#
# 前提：已在项目目录下执行过 git remote add origin <your-repo>

MSG=${1:-"update"}

echo "→ 校验图片列表（只读，不会写入）..."
if ! python3 update-all-lists.py; then
  echo ""
  echo "✗ 磁盘与 list.json 有差异，已中止发布（不会 commit/push）。"
  echo "  请先运行: python3 update-all-lists.py --import"
  echo "  确认导入结果无误后，再重新运行 ./publish.sh"
  exit 1
fi

echo "→ 检查未跟踪文件..."
UNTRACKED=$(git status --porcelain | grep '^??' | cut -c4-)
if [ -n "$UNTRACKED" ]; then
  echo ""
  echo "✗ 发现未跟踪文件，已中止发布（不会 add/commit/push）："
  echo "$UNTRACKED" | sed 's/^/  /'
  echo ""
  echo "  确认这些文件该不该提交后，手动 git add 再重新运行 ./publish.sh"
  exit 1
fi

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
