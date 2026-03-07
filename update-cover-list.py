#!/usr/bin/env python3
"""
扫描 assets/cover/ 里的图片，生成 list.json。
用法：python3 update-cover-list.py
把要轮播的图放进 assets/cover/ 后运行即可，无需改配置。
"""
import os
import json

dir_path = os.path.join(os.path.dirname(__file__), "assets", "cover")
exts = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
names = []

if os.path.isdir(dir_path):
    for f in os.listdir(dir_path):
        if f.startswith("."):
            continue
        if os.path.splitext(f)[1].lower() in exts:
            names.append(f)
    names.sort()

out_path = os.path.join(dir_path, "list.json")
os.makedirs(dir_path, exist_ok=True)
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(names, f, indent=2, ensure_ascii=False)

print("Wrote assets/cover/list.json:", len(names), "files:", names)
