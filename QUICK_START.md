# 📌 Hexo 博客快速参考

## ⚡ 最常用的 3 个命令

```bash
# 1️⃣ 创建新文章
hexo new post "文章标题"

# 2️⃣ 本地预览（http://localhost:4000）
npm run server

# 3️⃣ 一键发布到 GitHub
./deploy.sh "提交信息"
```

## 📁 重要文件位置

- **编写文章**: `~/Documents/blog/source/_posts/`
- **配置文件**: `~/Documents/blog/_config.yml`
- **部署脚本**: `~/Documents/blog/deploy.sh`
- **生成网站**: `~/Documents/blog/public/` (自动)

## 🔗 关键链接

- **博客首页**: https://infinitepwn.github.io
- **GitHub 仓库**: https://github.com/infinitepwn/infinitepwn.github.io
- **Source 分支**: 源代码备份
- **Main 分支**: GitHub Pages 发布

## 📝 文章模板

```markdown
---
title: 文章标题
date: 2026-03-31 19:30:00
categories:
  - 分类
tags:
  - 标签1
  - 标签2
---

正文内容从这里开始...
```

## 🚀 完整流程（复制粘贴版）

```bash
# 进入博客目录
cd ~/Documents/blog

# 创建文章
hexo new post "我的新文章"

# 编辑文章（用 VSCode 或其他编辑器打开）
code source/_posts/我的新文章.md

# 本地预览（可选）
npm run server
# 然后访问 http://localhost:4000

# 发布到 GitHub
./deploy.sh "发布：我的新文章"
```

## 🎨 支持的 Markdown 语法

```markdown
# 标题 1
## 标题 2
### 标题 3

**粗体**
*斜体*
~~删除线~~

- 列表项 1
- 列表项 2

1. 有序 1
2. 有序 2

> 引用文本

`代码`

\`\`\`javascript
// 代码块
console.log('Hello');
\`\`\`

[链接](https://example.com)
![图片](img.jpg)
```

## ⚙️ 其他 npm 命令

```bash
npm run clean      # 清理旧文件
npm run build      # 生成网站
npm run server     # 启动本地服务
npm run deploy     # 部署到 GitHub Pages
```

## 🔍 查看最新文章

```bash
# 列出所有文章
ls ~/Documents/blog/source/_posts/

# 编辑最后一篇文章
code $(ls -t ~/Documents/blog/source/_posts/ | head -1)
```

## 📱 在另一台电脑上继续编辑

```bash
git clone -b source https://github.com/infinitepwn/infinitepwn.github.io.git blog
cd blog && npm install
hexo new post "新文章"
./deploy.sh
```

## ✅ 检查清单

发布前确认：
- [ ] 文章标题清晰
- [ ] 分类和标签正确
- [ ] 本地预览效果满意
- [ ] 没有格式错误

---

**🎯 记住这一行就够了:**
```bash
cd ~/Documents/blog && hexo new post "标题" && npm run server && ./deploy.sh
```

**需要完整指南？** 查看 `BLOG_GUIDE.md`
