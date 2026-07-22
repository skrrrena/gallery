# Project: Serena Zhang Portfolio Website

## 项目概述
个人作品集网站，单文件 HTML + content.json 结构。仓库已连接 Netlify，push 到 main 后自动构建部署，不需要手动发布。涵盖 portrait photography 和 ceramics 两个方向。

## 写作指引
当撰写作品介绍、artist statement、about 页面、或任何网站文案时，参考 `.claude/writing-reference.md` 中的风格和结构。严格遵循其中的写作原则。

## 技术约束
- 单文件 HTML，dark literary aesthetic
- 内容存储在 content.json
- 中英双语，各自独立成文

## 协作规则
- 任何 `git push`（含 `./publish.sh`，它内部会 push）之前必须先问过用户，等明确同意再执行。
  测试、验证、演示场景都不例外——本地 commit 可以自由做，但只要涉及推送到远端，
  哪怕看起来是"顺手验证一下"，也要先问。
  起因：曾经为了测试 publish.sh 的中止逻辑而直接跑了 `./publish.sh`，
  结果因为测试文件命名疏忽（用了下划线开头的文件名，被扫描器按设计排除）导致
  中止逻辑没有触发，脚本走完整流程把一个测试用的杂散文件和一条无意义的
  commit message 真推送到了远端仓库。
