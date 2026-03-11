#!/usr/bin/env python3
"""
整理陶瓷图片到专属文件夹，并生成列表：

- 所有以 ceramics- 开头的图片（如 ceramics-01.jpg）会从 assets/ 根目录
  自动移动到 assets/ceramics/ 下面（只移动一次）
- 然后扫描 assets/ceramics/ 里的图片，生成 assets/ceramics/list.json

用法：python3 update-ceramics-list.py
把陶瓷图片放进 assets/ceramics/（或暂时放在 assets/ 并命名为 ceramics-xx.jpg），
然后运行本脚本；Ceramics 页面会自动使用这些图片。
"""
import os
import json
import shutil

ROOT = os.path.join(os.path.dirname(__file__), "assets")
CER_DIR = os.path.join(ROOT, "ceramics")
EXTS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}

os.makedirs(CER_DIR, exist_ok=True)

# 一次性把旧的 ceramics- 前缀图片从 assets/ 根目录挪到 assets/ceramics/
if os.path.isdir(ROOT):
    for name in os.listdir(ROOT):
        full = os.path.join(ROOT, name)
        if os.path.isdir(full):
            continue
        ext = os.path.splitext(name)[1].lower()
        if not (name.lower().startswith("ceramics-") and ext in EXTS):
            continue
        target = os.path.join(CER_DIR, name)
        if not os.path.exists(target):
            shutil.move(full, target)

# 生成 assets/ceramics/list.json
names: list[str] = []
if os.path.isdir(CER_DIR):
    for name in os.listdir(CER_DIR):
        if name.startswith("."):
            continue
        full = os.path.join(CER_DIR, name)
        if os.path.isdir(full):
            continue
        if os.path.splitext(name)[1].lower() in EXTS:
            names.append(name)
    names.sort()

out_path = os.path.join(CER_DIR, "list.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(names, f, indent=2, ensure_ascii=False)

print("Wrote assets/ceramics/list.json:", len(names), "files:", names)
