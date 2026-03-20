#!/usr/bin/env node
/**
 * 扫描 assets/cover/ 里的图片，生成 list.json。
 * 用法：node update-cover-list.js
 * 之后把 assets/cover/ 和 list.json 一起 git add 提交即可。
 */
const fs = require('fs');
const path = require('path');

const dir = path.join(__dirname, 'assets', 's1-ceramics', 'cover');
const exts = ['.jpg', '.jpeg', '.png', '.gif', '.webp'];
let names = [];

try {
  if (fs.existsSync(dir)) {
    names = fs.readdirSync(dir)
      .filter(f => {
        const ext = path.extname(f).toLowerCase();
        return exts.includes(ext) && !f.startsWith('.');
      })
      .sort();
  }
} catch (e) {
  console.error(e);
}

const outPath = path.join(dir, 'list.json');
fs.mkdirSync(dir, { recursive: true });
fs.writeFileSync(outPath, JSON.stringify(names, null, 2));
console.log('Wrote assets/cover/list.json:', names.length, 'files:', names);
