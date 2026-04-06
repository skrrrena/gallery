#!/usr/bin/env python3
# 扫描所有 assets/sN-xxx/ 的子文件夹，为每个子文件夹写 list.json
import os, json, re

IMAGE_EXTS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
assets_dir = os.path.join(os.path.dirname(__file__), 'assets')

def write_list_json(directory):
    files = sorted([
        f for f in os.listdir(directory)
        if not f.startswith('.')
        and os.path.isfile(os.path.join(directory, f))
        and os.path.splitext(f)[1].lower() in IMAGE_EXTS
    ])
    out_path = os.path.join(directory, 'list.json')
    with open(out_path, 'w') as fp:
        json.dump(files, fp, indent=2)
    rel = os.path.relpath(directory)
    preview = files[:3] + (['...'] if len(files) > 3 else [])
    print(f'Wrote {rel}/list.json: {len(files)} files: {preview}')

for name in os.listdir(assets_dir):
    if not re.match(r'^s\d+-', name):
        continue
    s_dir = os.path.join(assets_dir, name)
    if not os.path.isdir(s_dir):
        continue
    for sub in os.listdir(s_dir):
        if sub.startswith('.'):
            continue
        sub_dir = os.path.join(s_dir, sub)
        if os.path.isdir(sub_dir):
            write_list_json(sub_dir)
