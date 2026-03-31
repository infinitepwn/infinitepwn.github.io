# 🚀 macOS 上的 Hexo 博客完整指南

> 你的个人技术博客已经成功迁移到 macOS，并完全配置好！

---

## 📍 项目位置

```bash
~/Documents/blog/
```

## 🎯 项目结构

```
blog/
├── source/              # 博客源文件
│   └── _posts/         # 所有文章存放处 ⭐
├── public/             # 生成的静态网站（自动）
├── themes/             # 博客主题
├── scaffolds/          # 文章模板
├── _config.yml         # 主配置文件
├── package.json        # Node.js 配置
├── deploy.sh           # 一键部署脚本
└── node_modules/       # 依赖包
```

---

## ⚡ 快速开始（5 分钟）

### 1️⃣ 创建新文章

```bash
cd ~/Documents/blog
npm run clean && npm run build
# 或用快捷命令：
hexo new post "文章标题"
```

这会在 `source/_posts/` 生成一个 Markdown 文件。

### 2️⃣ 编辑文章

用你喜欢的编辑器打开新生成的文件，编写内容：

```markdown
---
title: 我的第一篇文章
date: 2026-03-31 19:30:00
categories:
  - 技术
tags:
  - Hexo
  - 博客
---

这里开始写文章内容...
```

### 3️⃣ 本地预览

```bash
npm run server
# 访问 http://localhost:4000
```

### 4️⃣ 一键发布 🎉

```bash
cd ~/Documents/blog
./deploy.sh "发布新文章"
```

或使用默认提交信息：

```bash
./deploy.sh
```

---

## 📝 常用 npm 命令

| 命令 | 作用 |
|------|------|
| `npm run clean` | 清理旧文件 |
| `npm run build` | 生成静态网站 |
| `npm run server` | 启动本地预览 |
| `npm run deploy` | 部署到 GitHub Pages |

---

## 🎨 文章模板参考

### 完整的前置信息（Front Matter）

```markdown
---
title: 文章标题
date: 2026-03-31 19:30:00          # 发布日期
updated: 2026-03-31 20:00:00       # 最后修改（可选）
categories:                         # 分类
  - 技术
  - 前端
tags:                               # 标签
  - JavaScript
  - React
description: "文章简介"            # SEO 描述
---

# 正文从这里开始

这是我的第一段话...
```

### 最简单的写法

```markdown
---
title: 简单标题
date: 2026-03-31
---

直接开始写内容...
```

---

## 🔄 完整的工作流

### 日常更新步骤

```bash
# 进入博客目录
cd ~/Documents/blog

# 创建新文章
hexo new post "今天的主题"

# 编辑文章（用 VSCode、Vim 或任何编辑器）
vim source/_posts/今天的主题.md

# 本地预览效果（可选）
npm run server
# 打开 http://localhost:4000 查看

# 满意后，一键发布！
./deploy.sh "完成今天的文章"

# 访问你的博客查看效果
# https://infinitepwn.github.io
```

---

## 🔐 两个分支的作用

你的仓库现在有两个分支：

| 分支 | 作用 | 内容 |
|------|------|------|
| **source** | 源代码管理 | Markdown 文章、配置、主题 |
| **main** | 发布分支 | 生成的 HTML 网站（GitHub Pages 读取） |

**重要**: 
- ✅ 编辑 source 分支中的文章
- ✅ 使用 `./deploy.sh` 自动处理两个分支
- ❌ 不要手动修改 main 分支（让部署脚本处理）

---

## 📱 在其他设备继续编辑

如果你想在另一台电脑上继续更新博客：

```bash
# 1. 克隆源代码分支
git clone -b source https://github.com/infinitepwn/infinitepwn.github.io.git blog

# 2. 进入目录
cd blog

# 3. 安装依赖
npm install

# 4. 开始编辑！
hexo new post "新文章"
./deploy.sh "发布文章"
```

---

## 🛠️ 常见问题

### Q1: 部署后博客没有更新？

**A**: 
1. 清除浏览器缓存：`Cmd+Shift+Delete`
2. 等待 1-2 分钟让 GitHub Pages 刷新
3. 强制刷新：`Cmd+Shift+R`
4. 检查部署日志：查看 deploy.sh 输出是否有错误

### Q2: 如何修改博客标题、作者等信息？

**A**: 编辑 `_config.yml` 文件：

```yaml
# Site
title: 你的新标题
author: 你的名字
description: 博客描述
```

然后重新部署：
```bash
npm run build
./deploy.sh "更新配置"
```

### Q3: 如何更换博客主题？

**A**: 
1. 从 [Hexo 主题库](https://hexo.io/themes/) 选择喜欢的主题
2. 根据主题说明安装到 `themes/` 目录
3. 修改 `_config.yml` 中的 `theme` 字段
4. 重新生成并部署

### Q4: 如何恢复之前在 Windows 上的文章？

**A**: 
- 如果还有源文件，复制到 `source/_posts/`
- 如果没有源文件，我可以帮你从已发布的 HTML 逆向提取

### Q5: Markdown 文件用什么编辑器？

**A**: 推荐：
- **VSCode** - 最好用，有预览功能
- **Sublime Text** - 轻量级
- **MacDown** - macOS 专用 Markdown 编辑器
- **vim/nano** - 终端编辑

---

## 💡 最佳实践

✅ **应该做**
- 经常提交（保留编辑历史）
- 使用有意义的提交信息
- 本地预览后再发布
- 定期备份重要文章
- 给文章添加合理的分类和标签

❌ **不要做**
- 手动编辑 `public/` 目录
- 直接修改 main 分支
- 忘记本地预览就发布
- 删除 `node_modules/` 后不重新 `npm install`

---

## 🚀 高级用法

### 创建草稿（不发布）

```bash
hexo new draft "我的草稿"
# 文件会在 source/_drafts/ 下

# 预览草稿
npm run server -- --draft

# 发布草稿
hexo publish draft "我的草稿"
```

### 创建页面（关于、友链等）

```bash
hexo new page "about"
# 会在 source/about/ 下创建 index.md

# 编辑 source/about/index.md 添加内容
```

### 添加分类和标签

在文章的 Front Matter 中：

```markdown
---
categories:
  - 前端
  - JavaScript   # 支持多级分类

tags:
  - React
  - TypeScript   # 支持多个标签
---
```

---

## 📊 查看博客统计

```bash
# 查看所有文章
ls ~/Documents/blog/source/_posts/

# 查看文章数量
ls -1 ~/Documents/blog/source/_posts/ | wc -l
```

---

## 🌐 分享到社交媒体

部署完成后，分享你的博客链接：

**博客地址**: https://infinitepwn.github.io  
**GitHub 仓库**: https://github.com/infinitepwn/infinitepwn.github.io

---

## 📞 需要帮助？

遇到问题可以：
1. 查看 [Hexo 官方文档](https://hexo.io/docs/)
2. 搜索 [Hexo 问题讨论](https://github.com/hexojs/hexo/issues)
3. 检查你的 `_config.yml` 配置是否正确

---

**祝你写博客愉快！** 🎉

更新于: 2026-03-31
