#!/usr/bin/env node
/**
 * 扫描 assets/amber/ 里的图片，生成 assets/amber/list.json
 *
 * 用法：node update-amber-list.js
 *
 * 添加 Amber 图片的工作流：
 * 1. 把新图片放进 assets/amber/
 * 2. 运行：node update-amber-list.js
 * 3. 提交并推送
 */
const fs = require('fs');
const path = require('path');

const amberDir = path.join(__dirname, 'assets', 's1-ceramics', 'amber');
const exts = ['.jpg', '.jpeg', '.png', '.gif', '.webp'];

if (!fs.existsSync(amberDir)) {
  fs.mkdirSync(amberDir, { recursive: true });
}

let names = [];
try {
  names = fs.readdirSync(amberDir)
    .filter(name => {
      if (name.startsWith('.')) return false;
      const full = path.join(amberDir, name);
      if (fs.statSync(full).isDirectory()) return false;
      return exts.includes(path.extname(name).toLowerCase());
    })
    .sort();
} catch (e) {
  console.error(e);
}

const outPath = path.join(amberDir, 'list.json');
fs.writeFileSync(outPath, JSON.stringify(names, null, 2));
console.log('Wrote assets/amber/list.json:', names.length, 'files:', names);
