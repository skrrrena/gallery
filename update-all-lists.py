#!/usr/bin/env python3
# 扫描所有 assets/sN-xxx/ 的子文件夹，为每个子文件夹更新 list.json。
#
# 与旧版本不同：这里是【合并】而不是全量覆盖——
# - 纯文件名数组格式的目录：保持这个格式不变，只是按磁盘现状增删文件名，
#   不会因为脚本重跑就丢数据（反正这个格式本来就没有额外字段）。
# - 对象数组格式的目录（例如 assets/s1-ceramics/grid，含 id/title/desc/
#   details/hidden 等字段）：已有条目按 main 文件名匹配，完整保留其所有
#   字段；条目的 details 里磁盘上已不存在的文件会被剔除；main 文件被删除
#   的条目整条移除；磁盘上新出现且未被任何已有条目引用的文件，作为新
#   条目追加在末尾（hidden 默认 false，details 默认为空）。
# - 两种格式都会排除自动生成的 -thumb 缩略图文件和 *_poster.* 视频封面帧，
#   不会被误认成新图；下划线开头的子目录（如 _hidden/）整个不扫描，
#   放在里面的文件不会进入 list.json。
import os, json, re

IMAGE_EXTS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
THUMB_RE = re.compile(r'-thumb\.[^.]+$', re.IGNORECASE)
POSTER_RE = re.compile(r'_poster\.[^.]+$', re.IGNORECASE)
assets_dir = os.path.join(os.path.dirname(__file__), 'assets')


def title_from_filename(name):
    base = re.sub(r'\.[^.]+$', '', name)
    base = re.sub(r'[-_]', ' ', base)
    return base or name


def slugify(name):
    s = title_from_filename(name).lower().strip()
    s = re.sub(r'[^a-z0-9]+', '-', s)
    s = s.strip('-')
    return s or 'item'


def make_entry(filename):
    return {
        'id': slugify(filename),
        'main': filename,
        'title': title_from_filename(filename),
        'title_zh': '',
        'title_ja': '',
        'desc': '',
        'desc_zh': '',
        'desc_ja': '',
        'details': [],
        'hidden': False,
    }


def scan_files(directory):
    files = []
    for f in os.listdir(directory):
        if f.startswith('.'):
            continue
        if f.startswith('_'):
            continue
        full = os.path.join(directory, f)
        if os.path.isdir(full):
            continue
        if os.path.splitext(f)[1].lower() not in IMAGE_EXTS:
            continue
        if THUMB_RE.search(f) or POSTER_RE.search(f):
            continue
        files.append(f)
    return sorted(files)


def load_existing(out_path):
    if not os.path.exists(out_path):
        return []
    try:
        with open(out_path) as fp:
            raw = json.load(fp)
        return raw if isinstance(raw, list) else []
    except Exception as e:
        print(f'  ! 无法解析现有 {os.path.relpath(out_path)}，将视为空列表: {e}')
        return []


def write_json(out_path, data):
    with open(out_path, 'w') as fp:
        json.dump(data, fp, indent=2, ensure_ascii=False)
        fp.write('\n')


def merge_object_format(directory, out_path, existing, files, files_on_disk):
    normalized = [e if isinstance(e, dict) else make_entry(e) for e in existing]
    referenced = set()
    kept = []
    for entry in normalized:
        main = entry.get('main')
        if not main or main not in files_on_disk:
            continue
        if 'hidden' not in entry:
            entry['hidden'] = False
        details = entry.get('details')
        entry['details'] = [f for f in details if f in files_on_disk] if isinstance(details, list) else []
        referenced.add(main)
        referenced.update(entry['details'])
        kept.append(entry)

    new_entries = [make_entry(f) for f in files if f not in referenced]
    result = kept + new_entries
    write_json(out_path, result)

    rel = os.path.relpath(directory)
    removed = len(normalized) - len(kept)
    print(f'Wrote {rel}/list.json (object format): {len(result)} entries '
          f'({len(kept)} kept, {len(new_entries)} new), {removed} removed')


def merge_flat_format(directory, out_path, existing, files, files_on_disk):
    existing_flat = [e for e in existing if isinstance(e, str)]
    kept = [f for f in existing_flat if f in files_on_disk]
    kept_set = set(kept)
    new_entries = [f for f in files if f not in kept_set]
    result = sorted(kept + new_entries)
    write_json(out_path, result)

    rel = os.path.relpath(directory)
    removed = len(existing_flat) - len(kept)
    preview = result[:3] + (['...'] if len(result) > 3 else [])
    print(f'Wrote {rel}/list.json: {len(result)} files '
          f'({len(kept)} kept, {len(new_entries)} new, {removed} removed): {preview}')


def write_list_json(directory):
    files = scan_files(directory)
    files_on_disk = set(files)
    out_path = os.path.join(directory, 'list.json')
    existing = load_existing(out_path)

    is_object_format = any(isinstance(e, dict) for e in existing)
    if is_object_format:
        merge_object_format(directory, out_path, existing, files, files_on_disk)
    else:
        merge_flat_format(directory, out_path, existing, files, files_on_disk)


for name in os.listdir(assets_dir):
    if not re.match(r'^s\d+-', name):
        continue
    s_dir = os.path.join(assets_dir, name)
    if not os.path.isdir(s_dir):
        continue
    for sub in os.listdir(s_dir):
        if sub.startswith('.') or sub.startswith('_'):
            continue
        sub_dir = os.path.join(s_dir, sub)
        if os.path.isdir(sub_dir):
            write_list_json(sub_dir)
