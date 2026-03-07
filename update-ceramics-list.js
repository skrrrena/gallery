#!/usr/bin/env node
/**
 * 扫描 assets/ 里的图片（不含 cover 子文件夹），生成 ceramics-list.json。
 * 用法：node update-ceramics-list.js
 * 放在 assets/ 的图都会出现在 ceramics 页面网格里。
 */
const fs = require('fs');
const path = require('path');

const dir = path.join(__dirname, 'assets');
const exts = ['.jpg', '.jpeg', '.png', '.gif', '.webp'];
let names = [];

try {
  if (fs.existsSync(dir)) {
    names = fs.readdirSync(dir)
      .filter(f => {
        if (f === 'list.json' || f === 'ceramics-list.json' || f.startsWith('.')) return false;
        const full = path.join(dir, f);
        if (fs.statSync(full).isDirectory()) return false; // 不含 cover 等子文件夹
        return exts.includes(path.extname(f).toLowerCase());
      })
      .sort();
  }
} catch (e) {
  console.error(e);
}

const outPath = path.join(dir, 'ceramics-list.json');
fs.writeFileSync(outPath, JSON.stringify(names, null, 2));
console.log('Wrote assets/ceramics-list.json:', names.length, 'files:', names);
