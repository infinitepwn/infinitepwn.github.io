#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import os
from pathlib import Path
import shutil

# 映射：Typora 临时文件 -> 图床中的对应名称
# 这些图片应该已经在你的备份中

html_file = "/Users/infinite/Documents/blog-backup/post/20250820151101.html"
markdown_file = "/Users/infinite/Documents/blog/source/_posts/2025-08-20_SWPU-NSSCTF2025.md"
backup_post_dir = "/Users/infinite/Documents/blog-backup/post/20250820151101"

# 首先，从HTML中提取所有图片信息
with open(html_file, 'r', encoding='utf-8') as f:
    html_content = f.read()

# 提取所有图片
image_pattern = r'src="([^"]*(?:\.(png|jpg|jpeg|gif))?)"'
matches = re.findall(image_pattern, html_content)

# 分类图片
local_images = []  # Windows路径的本地图片
cdn_images = []    # CDN上的图片

for match in matches:
    src = match[0]
    if 'Typora' in src or src.startswith('C:'):
        local_images.append(src)
    elif 'cdn.jsdelivr.net' in src or 'raw.githubusercontent.com' in src:
        cdn_images.append(src)

print(f"找到 {len(local_images)} 张本地图片")
print(f"找到 {len(cdn_images)} 张CDN图片")

# 从HTML中提取图片（替换Windows路径为CDN链接）
# 首先检查备份目录中是否有这些图片
backup_images = {}
if os.path.exists(backup_post_dir):
    for root, dirs, files in os.walk(backup_post_dir):
        for file in files:
            if file.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                file_path = os.path.join(root, file)
                backup_images[file] = file_path
                print(f"  找到备份图片: {file}")

print(f"\n备份目录中共有 {len(backup_images)} 张图片")

# 从HTML中提取所有img标签并创建引用
img_tags = re.findall(r'<img[^>]*src="([^"]*)"[^>]*alt="([^"]*)"', html_content)

print(f"\n从HTML提取到 {len(img_tags)} 张图片")

# 读取Markdown文件
with open(markdown_file, 'r', encoding='utf-8') as f:
    md_content = f.read()

# 对于每张图片，如果是本地路径，替换为CDN链接
# 首先，我们需要将这些图片上传到图床
blogimage_dir = os.path.expanduser("~/blogimage")

for src, alt in img_tags:
    if 'Typora' in src or src.startswith('C:'):
        # 这是一张本地图片
        # 从备份中找到对应的文件
        filename = os.path.basename(src)
        if filename in backup_images:
            src_file = backup_images[filename]
            dst_file = os.path.join(blogimage_dir, filename)
            
            # 复制到图床
            if not os.path.exists(dst_file):
                shutil.copy(src_file, dst_file)
                print(f"✓ 复制图片: {filename}")

# 现在从HTML中提取图片引用并添加到Markdown
img_references = {}

# 更复杂的HTML解析：查找所有的图片标签
import re
html_img_pattern = r'<img[^>]*?(?:src|data-src)="([^"]*\.(?:png|jpg|jpeg|gif))"[^>]*?(?:alt|title)="([^"]*)"'
html_img_matches = re.findall(html_img_pattern, html_content, re.IGNORECASE)

for src, alt in html_img_matches:
    if src not in img_references:
        # 转换Windows路径为CDN路径
        filename = os.path.basename(src)
        if 'Typora' in src or src.startswith('C:'):
            cdn_url = f"https://raw.githubusercontent.com/infinitepwn/blogimage/main/{filename}"
        else:
            cdn_url = src
        
        img_references[src] = (cdn_url, alt)

print(f"\n识别到 {len(img_references)} 条图片引用")

# 遍历Markdown中的所有段落，在合适的位置添加图片
# 这里我们采用简单的策略：在代码块后面添加图片

sections = md_content.split('## ')
new_content = sections[0]  # 保留头部

for section in sections[1:]:
    new_content += '## ' + section
    
    # 检查这个section中是否应该有图片
    # 通过检查HTML备份来判断

# 实际上，更好的方法是直接从HTML中提取纯文本后的图片

# 让我们改用另一种策略：直接在Markdown适当位置插入图片
# 首先读取HTML并转换为Markdown格式

from html.parser import HTMLParser

class ImageExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []
        self.current_h2 = None
        self.in_content = False
        
    def handle_starttag(self, tag, attrs):
        if tag == 'h2':
            self.in_content = True
            for attr, value in attrs:
                if attr == 'id':
                    self.current_h2 = value
        elif tag == 'img' and self.in_content:
            for attr, value in attrs:
                if attr in ['src', 'data-src']:
                    filename = os.path.basename(value)
                    self.images.append((self.current_h2, value, filename))

# 提取器
extractor = ImageExtractor()
extractor.feed(html_content)

# 按照section组织图片
image_by_section = {}
for section, src, filename in extractor.images:
    if section not in image_by_section:
        image_by_section[section] = []
    image_by_section[section].append((src, filename))

print(f"\n按section统计图片:")
for section, images in image_by_section.items():
    print(f"  {section}: {len(images)} 张")

# 现在添加图片到Markdown
# 策略：在每个## 小节的末尾添加这个小节的所有图片

for section in image_by_section:
    for src, filename in image_by_section[section]:
        # 构建CDN URL
        cdn_url = f"https://raw.githubusercontent.com/infinitepwn/blogimage/main/{filename}"
        
        # 在Markdown中找到这个section的结束位置，添加图片
        # 简化处理：直接在Markdown末尾添加
        pass

# 实际上，让我们用更直接的方法
# 直接从HTML中提取所有img标签，然后在Markdown相应位置插入

print("\n正在添加图片引用到Markdown...")

# 在Markdown末尾添加所有图片
for section, images in sorted(image_by_section.items()):
    md_content += f"\n\n### 图片资源 - {section}\n"
    for src, filename in images:
        cdn_url = f"https://raw.githubusercontent.com/infinitepwn/blogimage/main/{filename}"
        md_content += f"\n![{filename}]({cdn_url})\n"

# 保存更新后的Markdown
with open(markdown_file, 'w', encoding='utf-8') as f:
    f.write(md_content)

print(f"✓ 已更新Markdown文件")

# 现在上传图片到GitHub
print("\n正在提交图片到GitHub...")
os.system(f"cd ~/blogimage && git add . && git commit -m 'Add SWPU-NSSCTF images' && git push origin main 2>&1 | tail -5")

print("\n✅ 完成！")
