#!/usr/bin/env python3
"""
扫描 assets/ 里的图片（不含 cover 子文件夹），生成 ceramics-list.json。
用法：python3 update-ceramics-list.py
放在 assets/ 的图都会出现在 ceramics 页面网格里。
"""
import os
import json

dir_path = os.path.join(os.path.dirname(__file__), "assets")
exts = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
names = []

if os.path.isdir(dir_path):
    for f in os.listdir(dir_path):
        if f in ("list.json", "ceramics-list.json") or f.startswith("."):
            continue
        full = os.path.join(dir_path, f)
        if os.path.isdir(full):
            continue
        if os.path.splitext(f)[1].lower() in exts:
            names.append(f)
    names.sort()

out_path = os.path.join(dir_path, "ceramics-list.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(names, f, indent=2, ensure_ascii=False)

print("Wrote assets/ceramics-list.json:", len(names), "files:", names)
