#!/usr/bin/env node
/**
 * 整理陶瓷图片到 assets/ceramics/ 并生成列表：
 *
 * - 把 assets/ 里以 ceramics- 开头的图片移到 assets/ceramics/（只移动一次）
 * - 扫描 assets/ceramics/ 里的图片，生成 assets/ceramics/list.json
 *
 * 用法：node update-ceramics-list.js
 */
const fs = require('fs');
const path = require('path');

const rootDir = path.join(__dirname, 'assets');
const cerDir = path.join(rootDir, 'ceramics');
const exts = ['.jpg', '.jpeg', '.png', '.gif', '.webp'];

if (!fs.existsSync(cerDir)) {
  fs.mkdirSync(cerDir, { recursive: true });
}

// 一次性把旧的 ceramics- 前缀图片从 assets/ 根目录挪到 assets/ceramics/
if (fs.existsSync(rootDir)) {
  for (const name of fs.readdirSync(rootDir)) {
    const full = path.join(rootDir, name);
    if (fs.statSync(full).isDirectory()) continue;
    const ext = path.extname(name).toLowerCase();
    if (!name.toLowerCase().startsWith('ceramics-') || !exts.includes(ext)) continue;
    const target = path.join(cerDir, name);
    if (!fs.existsSync(target)) {
      fs.renameSync(full, target);
    }
  }
}

// 生成 assets/ceramics/list.json
let names = [];
try {
  if (fs.existsSync(cerDir)) {
    names = fs.readdirSync(cerDir)
      .filter(name => {
        if (name.startsWith('.')) return false;
        const full = path.join(cerDir, name);
        if (fs.statSync(full).isDirectory()) return false;
        return exts.includes(path.extname(name).toLowerCase());
      })
      .sort();
  }
} catch (e) {
  console.error(e);
}

const outPath = path.join(cerDir, 'list.json');
fs.writeFileSync(outPath, JSON.stringify(names, null, 2));
console.log('Wrote assets/ceramics/list.json:', names.length, 'files:', names);
