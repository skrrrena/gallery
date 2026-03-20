#!/usr/bin/env node
// 扫描所有 assets/sN-xxx/ 的子文件夹，为每个子文件夹写 list.json（图片文件列表）。
// 替代 update-cover-list.js / update-ceramics-list.js / update-vermilion-list.js /
//        update-amber-list.js / update-portraiture-list.js
//
// 用法：node update-all-lists.js
// 添加图片后运行一次即可，publish.sh 会自动调用。
const fs   = require('fs');
const path = require('path');

const IMAGE_EXTS = new Set(['.jpg','.jpeg','.png','.gif','.webp','.JPG','.JPEG','.PNG','.GIF','.WEBP']);
const assetsDir  = path.join(__dirname, 'assets');

function writeListJson(dir) {
  const files = fs.readdirSync(dir)
    .filter(f => {
      if (f.startsWith('.')) return false;
      if (fs.statSync(path.join(dir, f)).isDirectory()) return false;
      return IMAGE_EXTS.has(path.extname(f));
    })
    .sort();
  const outPath = path.join(dir, 'list.json');
  fs.writeFileSync(outPath, JSON.stringify(files, null, 2));
  const rel = path.relative(__dirname, dir);
  const preview = files.length > 3 ? files.slice(0, 3).concat(['...']) : files;
  console.log('Wrote ' + rel + '/list.json:', files.length, 'files:', preview);
}

// Find all sN-* top-level dirs under assets/
const sNDirs = fs.readdirSync(assetsDir)
  .filter(name => /^s\d+-/.test(name))
  .map(name => path.join(assetsDir, name))
  .filter(p => fs.statSync(p).isDirectory());

for (const sDir of sNDirs) {
  // Scan every direct subdirectory
  const subDirs = fs.readdirSync(sDir)
    .filter(name => {
      if (name.startsWith('.')) return false;
      return fs.statSync(path.join(sDir, name)).isDirectory();
    });
  for (const sub of subDirs) {
    writeListJson(path.join(sDir, sub));
  }
}
