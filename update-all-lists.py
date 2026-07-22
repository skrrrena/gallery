#!/usr/bin/env python3
# 校验/导入 assets/sN-xxx/ 各子文件夹的 list.json 与磁盘文件的差异。
#
# list.json 是仓库里的权威内容（后台/CMS 直接编辑它），这个脚本不再是
# 自动生成器，默认只做只读校验：
# - 报告每个目录里磁盘上有但 list.json 没有的新文件、list.json 里有但
#   磁盘上已经没有的条目，不写入任何文件。
#
# 加 --import 才会真正写入，写入规则：
# - 已有条目保持原有位置和全部字段不变（不做任何字段级修改）。
# - 磁盘上已不存在的条目（对象格式按 main，纯文件名格式按文件名本身）
#   整条移除。
# - 磁盘上新出现、且未被任何已有条目引用（含 details 里的文件）的文件，
#   按文件名排序后追加在末尾。纯文件名数组格式和对象数组格式使用同一
#   套规则，都不会对已有条目重新排序。
# - 两种格式都会排除自动生成的 -thumb 缩略图文件和 *_poster.* 视频封面
#   帧；下划线开头的子目录（如 _hidden/）整个不扫描，里面的文件不会
#   进入 list.json。
import os, json, re, argparse

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


def merge_object_format(existing, files, files_on_disk):
    normalized = [e if isinstance(e, dict) else make_entry(e) for e in existing]
    kept = []
    removed = []
    referenced = set()
    for entry in normalized:
        main = entry.get('main')
        if not main or main not in files_on_disk:
            if main:
                removed.append(main)
            continue
        referenced.add(main)
        details = entry.get('details')
        if isinstance(details, list):
            referenced.update(details)
        kept.append(entry)  # 原样保留，不修改任何字段

    new_entries = [make_entry(f) for f in files if f not in referenced]
    result = kept + new_entries
    added = [e['main'] for e in new_entries]
    return result, added, removed


def merge_flat_format(existing, files, files_on_disk):
    existing_flat = [e for e in existing if isinstance(e, str)]
    kept = [f for f in existing_flat if f in files_on_disk]
    kept_set = set(kept)
    new_entries = sorted(f for f in files if f not in kept_set)
    result = kept + new_entries  # 只在已有顺序后追加新文件，不整体重排
    removed = [f for f in existing_flat if f not in files_on_disk]
    return result, new_entries, removed


def process_directory(directory, do_import):
    files = scan_files(directory)
    files_on_disk = set(files)
    out_path = os.path.join(directory, 'list.json')
    existing = load_existing(out_path)
    is_object_format = any(isinstance(e, dict) for e in existing)

    if is_object_format:
        result, added, removed = merge_object_format(existing, files, files_on_disk)
    else:
        result, added, removed = merge_flat_format(existing, files, files_on_disk)

    rel = os.path.relpath(directory)
    if not added and not removed:
        return False

    kind = 'object' if is_object_format else 'flat'
    print(f'  {rel} ({kind}): +{len(added)} new, -{len(removed)} removed')
    if added:
        print(f'    + {added}')
    if removed:
        print(f'    - {removed}')

    if do_import:
        write_json(out_path, result)
        print(f'    -> 已写入')

    return True


def main():
    parser = argparse.ArgumentParser(
        description='校验/导入 assets 下各目录 list.json 与磁盘文件的差异。'
                    '默认只读校验，不写入任何文件；加 --import 才会写入。')
    parser.add_argument('--import', dest='do_import', action='store_true',
                        help='写入变更（新增/移除条目）。不加此参数时仅报告差异。')
    args = parser.parse_args()

    print('模式：' + ('导入（会写入）' if args.do_import else '只读校验（不写入）'))
    print()

    any_diff = False
    for name in sorted(os.listdir(assets_dir)):
        if not re.match(r'^s\d+-', name):
            continue
        s_dir = os.path.join(assets_dir, name)
        if not os.path.isdir(s_dir):
            continue
        for sub in sorted(os.listdir(s_dir)):
            if sub.startswith('.') or sub.startswith('_'):
                continue
            sub_dir = os.path.join(s_dir, sub)
            if os.path.isdir(sub_dir):
                if process_directory(sub_dir, args.do_import):
                    any_diff = True

    print()
    if not any_diff:
        print('所有目录与磁盘一致，无差异。')
        return 0
    if args.do_import:
        return 0
    print('以上为只读校验结果，未写入任何文件。加 --import 参数执行导入。')
    return 1


if __name__ == '__main__':
    raise SystemExit(main())
