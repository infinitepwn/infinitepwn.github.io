# ✅ 文章恢复完成！

## 📊 恢复统计

| 项目 | 数量 |
|------|------|
| **恢复的文章** | 57 篇 |
| **生成的页面** | 106 个 |
| **恢复状态** | ✅ 完成 |

## 🔍 恢复方法

由于你没有原始的 Markdown 源文件，我采用了以下方案：

1. **HTML 提取** - 从已发布的 HTML 文件中提取元数据（标题、日期等）
2. **Markdown 转换** - 生成 Markdown 格式的文章模板
3. **内容保留** - 保留每篇文章的开头部分和关键信息

> ⚠️ **注意**: 提取的文章只包含基本内容预览。完整的格式化内容（代码块、列表、表格等）可能需要手动调整。

## 🗂️ 恢复的文章分类

### CTF 和竞赛相关
- BYUCTF2025 crypto wp
- GHCTF2025wp
- H&NCTF2025 / H&NCTF2025-crypto
- XYCTF
- 黄河流域wp
- 轩辕杯crypto-wp
- 等等...

### 密码学和算法
- RSA相关总结
- RSA选择密文攻击
- Coppersmith归纳
- LWE学习
- lattice 相关
- Hash 长度拓展攻击
- 等等...

### 编程基础
- 递归和迭代的区别
- 数据结构与算法笔记
- 二叉树
- 有向图笔记
- 外排序
- 等等...

### 工具和技术
- openssl使用
- sympy库的使用
- z3的使用
- reverse常见函数
- 等等...

## 📁 文件位置

```
~/Documents/blog/source/_posts/
├── array.md
├── pointer.md
├── recurision.md
├── RSA相关总结.md
├── 数据结构与算法笔记.md
├── ... 共 58 个文件
```

## 🚀 后续步骤

### 1️⃣ 检查和调整文章内容

打开任何文章查看格式：

```bash
code ~/Documents/blog/source/_posts/RSA相关总结.md
```

### 2️⃣ 修复格式问题

- 检查代码块的语法高亮
- 调整表格和列表格式
- 补充缺失的图片和链接

### 3️⃣ 添加分类和标签

编辑文章的 Front Matter：

```markdown
---
title: 文章标题
date: 2025-03-31 20:00:00
categories:
  - 正确的分类
tags:
  - 重要标签
---
```

### 4️⃣ 重新发布

修改完成后：

```bash
cd ~/Documents/blog
./deploy.sh "修复文章格式和内容"
```

## 📝 提取脚本

如果将来需要再次提取，脚本已保存在：

```bash
~/Documents/blog/extract_articles.py
```

使用方法：

```bash
python3 ~/Documents/blog/extract_articles.py
```

## ✨ 已发布的内容

你的博客已经包含所有恢复的文章，可以在以下地址访问：

**https://infinitepwn.github.io**

## 🔗 Git 分支状态

- ✅ **source 分支** - 包含所有恢复的源文件
- ✅ **main 分支** - 已部署到 GitHub Pages

## 💡 建议

1. **优先级修复**：
   - 首先修复重要文章的格式
   - 然后逐个调整其他文章

2. **批量操作**：
   - 可以用脚本批量更新分类和标签
   - 可以用正则表达式修复常见格式问题

3. **备份**：
   - 你的源代码已在 source 分支
   - 每次修改后记得 `git push origin source`

---

**需要帮助修复文章格式？** 告诉我！🎉

