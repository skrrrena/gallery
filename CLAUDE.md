# Project: Serena Zhang Portfolio Website

## 项目概述
个人作品集网站，单文件 HTML + content.json 结构。仓库已连接 Netlify，push 到 main 后自动构建部署，不需要手动发布。涵盖 portrait photography 和 ceramics 两个方向。

## 写作指引
当撰写作品介绍、artist statement、about 页面、或任何网站文案时，参考 `.claude/writing-reference.md` 中的风格和结构。严格遵循其中的写作原则。

## 技术约束
- 单文件 HTML，dark literary aesthetic
- 内容存储在 content.json
- 中英双语，各自独立成文

## 推送规则

默认直接 push，不用问。这是个人作品集站，改错了可以 revert，
Netlify 也能回滚部署，代价很低。

以下情况必须先问我，得到明确同意再执行：

1. 任何 force push、rebase、amend 已推送的 commit、或其它改写已推送历史的操作
2. commit 里包含任何形式的密钥、token、API key、密码
   （包括示例值、占位符、注释掉的）
3. 单个二进制文件超过 2MB，或本次 commit 新增的二进制总量超过 5MB
4. 删除不是本次会话创建的文件（不含明确交办的删除任务）
5. 删除或重命名分支

另外两条硬性要求，任何时候都适用：

- commit message 必须是描述实际改动的正经句子。
  禁止 "test"、"wip"、"should not happen"、"tmp" 这类占位内容。
  如果一个改动不值得写正经 message，那它就不该被提交。
- 测试和验证一律在本地进行，绝不推送。需要验证部署效果时，
  先告诉我你要推什么、验证什么，然后再推。
