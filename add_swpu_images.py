#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import os
from html.parser import HTMLParser

html_file = "/Users/infinite/Documents/blog-backup/post/20250820151101.html"
markdown_file = "/Users/infinite/Documents/blog/source/_posts/2025-08-20_SWPU-NSSCTF2025.md"

# 从HTML中提取所有图片
with open(html_file, 'r', encoding='utf-8') as f:
    html_content = f.read()

# 使用正则表达式提取所有img标签
img_pattern = r'<img[^>]*?src="([^"]+)"[^>]*?alt="([^"]*)"'
img_matches = re.findall(img_pattern, html_content)

print(f"从HTML中找到 {len(img_matches)} 张图片引用")

# 分类：CDN图片 vs 本地图片
cdn_images = []
local_images = []

for src, alt in img_matches:
    if 'cdn.jsdelivr.net' in src:
        cdn_images.append((src, alt))
    elif src.startswith('C:') or 'Typora' in src:
        local_images.append((src, alt))

print(f"  CDN上的: {len(cdn_images)} 张")
print(f"  本地/丢失: {len(local_images)} 张")

# 读取Markdown文件
with open(markdown_file, 'r', encoding='utf-8') as f:
    md_content = f.read()

# 在文件末尾添加图片部分
md_content += "\n\n---\n\n## 📎 图片资源\n\n"

if cdn_images:
    md_content += "### ✅ CDN上的图片\n\n"
    for src, alt in cdn_images:
        # 提取文件名
        filename = os.path.basename(src)
        md_content += f"![{alt or filename}]({src})\n\n"

if local_images:
    md_content += "### ⚠️ 丢失的本地图片（共 {} 张）\n\n".format(len(local_images))
    md_content += "_这些图片在原始Windows环境中，目前已丢失。如果你能找到这些文件的备份，可以上传到图床后恢复。_\n\n"
    
    lost_files = set()
    for src, alt in local_images:
        filename = os.path.basename(src)
        lost_files.add(filename)
    
    for filename in sorted(lost_files):
        md_content += f"- `{filename}`\n"

# 保存更新后的Markdown
with open(markdown_file, 'w', encoding='utf-8') as f:
    f.write(md_content)

print(f"\n✓ 已更新Markdown文件")
print(f"  - 添加了 {len(cdn_images)} 张CDN图片")
print(f"  - 标记了 {len(local_images)} 张丢失的本地图片")
