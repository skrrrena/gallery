#!/usr/bin/env node
/**
 * 扫描 assets/vermilion/ 里的图片，生成 assets/vermilion/list.json
 *
 * 用法：node update-vermilion-list.js
 *
 * 添加 Vermilion 图片的工作流：
 * 1. 把新图片放进 assets/vermilion/
 * 2. 运行：node update-vermilion-list.js
 * 3. 提交并推送
 */
const fs = require('fs');
const path = require('path');

const verDir = path.join(__dirname, 'assets', 'vermilion');
const exts = ['.jpg', '.jpeg', '.png', '.gif', '.webp'];

if (!fs.existsSync(verDir)) {
  fs.mkdirSync(verDir, { recursive: true });
}

let names = [];
try {
  names = fs.readdirSync(verDir)
    .filter(name => {
      if (name.startsWith('.')) return false;
      const full = path.join(verDir, name);
      if (fs.statSync(full).isDirectory()) return false;
      return exts.includes(path.extname(name).toLowerCase());
    })
    .sort();
} catch (e) {
  console.error(e);
}

const outPath = path.join(verDir, 'list.json');
fs.writeFileSync(outPath, JSON.stringify(names, null, 2));
console.log('Wrote assets/vermilion/list.json:', names.length, 'files:', names);
