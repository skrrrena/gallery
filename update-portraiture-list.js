#!/usr/bin/env node
/**
 * 扫描 assets/s2-portraiture/ 里的图片，生成 assets/s2-portraiture/list.json
 *
 * 用法：node update-portraiture-list.js
 *
 * 添加 Portraiture 图片的工作流：
 * 1. 把新图片放进 assets/s2-portraiture/
 * 2. 运行：node update-portraiture-list.js
 * 3. 提交并推送
 */
const fs = require('fs');
const path = require('path');

const dir = path.join(__dirname, 'assets', 's2-portraiture');
const exts = ['.jpg', '.jpeg', '.png', '.gif', '.webp'];

if (!fs.existsSync(dir)) {
  fs.mkdirSync(dir, { recursive: true });
}

let names = [];
try {
  names = fs.readdirSync(dir)
    .filter(name => {
      if (name.startsWith('.')) return false;
      const full = path.join(dir, name);
      if (fs.statSync(full).isDirectory()) return false;
      return exts.includes(path.extname(name).toLowerCase());
    })
    .sort();
} catch (e) {
  console.error(e);
}

const outPath = path.join(dir, 'list.json');
fs.writeFileSync(outPath, JSON.stringify(names, null, 2));
console.log('Wrote assets/s2-portraiture/list.json:', names.length, 'files:', names);
