#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量添加所有图片到图床并更新文章
"""

import os
import re
from pathlib import Path
from bs4 import BeautifulSoup
import shutil

CDN_BASE = "https://raw.githubusercontent.com/infinitepwn/blogimage/main"
BLOGIMAGE_DIR = Path(os.path.expanduser("~/blogimage"))
HTML_BACKUP_DIR = Path(os.path.expanduser("~/Documents/blog-backup/post"))
POSTS_DIR = Path(os.path.expanduser("~/Documents/blog/source/_posts"))

def get_images_from_html(html_file):
    """从HTML文件中提取图片信息及其所在的文章信息"""
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
        
        # 获取文章标题和日期
        title_tag = soup.find('meta', property='og:title')
        title = title_tag.get('content', '') if title_tag else ''
        
        published_tag = soup.find('meta', property='article:published_time')
        published = published_tag.get('content', '') if published_tag else ''
        
        # 提取图片
        images = []
        article = soup.find('article', class_='post-content')
        if article:
            for img in article.find_all('img'):
                src = img.get('src', '')
                alt = img.get('alt', 'image')
                
                # 只处理相对路径且是文章内容的图片
                if src and src.startswith('/') and '/' in src[1:]:
                    if not any(x in src for x in ['img/head', '/js/', '/css/', '/api/']):
                        images.append({
                            'src': src,
                            'alt': alt,
                            'filename': src.split('/')[-1]
                        })
        
        return {
            'title': title,
            'published': published,
            'images': images,
            'html_file': html_file
        }
    except Exception as e:
        print(f"Error reading {html_file}: {e}")
        return None

def copy_image_file(filename):
    """查找并复制图片文件到图床"""
    # 在 post 目录下查找
    for post_dir in HTML_BACKUP_DIR.glob('*/'):
        img_path = post_dir / filename
        if img_path.exists():
            dest = BLOGIMAGE_DIR / filename
            if not dest.exists():
                shutil.copy2(img_path, dest)
                print(f"    ✓ 已复制: {filename}")
            else:
                print(f"    ⊘ 已存在: {filename}")
            return True
    
    print(f"    ✗ 未找到: {filename}")
    return False

def find_article_file(title, published):
    """根据标题和日期查找对应的Markdown文件"""
    if published:
        try:
            # 提取日期前缀 YYYY-MM-DD
            date_prefix = published.split('T')[0]
            # 查找以该日期开头的文件
            for md_file in POSTS_DIR.glob(f"{date_prefix}_*.md"):
                return md_file
        except:
            pass
    
    # 如果没找到，尝试模糊匹配标题
    clean_title = re.sub(r'[^\w\u4e00-\u9fff\s-]', '', title)
    for md_file in POSTS_DIR.glob('*.md'):
        if clean_title.lower() in md_file.name.lower() or md_file.name.lower() in clean_title.lower():
            return md_file
    
    return None

def add_images_to_article(md_file, images):
    """将图片引用添加到文章中"""
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否已有这些图片
    images_to_add = []
    for img in images:
        if img['filename'] not in content:
            images_to_add.append(img)
    
    if not images_to_add:
        return False
    
    # 在Front Matter之后添加所有图片
    parts = content.split('---', 2)
    if len(parts) == 3:
        # 构建图片markdown
        img_md = ''
        for img in images_to_add:
            cdn_url = f"{CDN_BASE}/{img['filename']}"
            img_md += f"![{img['alt']}]({cdn_url})\n\n"
        
        new_content = '---' + parts[1] + '---\n\n' + img_md + parts[2]
    else:
        # 没有Front Matter
        img_md = ''
        for img in images_to_add:
            cdn_url = f"{CDN_BASE}/{img['filename']}"
            img_md += f"![{img['alt']}]({cdn_url})\n\n"
        new_content = img_md + content
    
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return len(images_to_add)

def main():
    html_files = sorted(HTML_BACKUP_DIR.glob('*.html'))
    
    print(f"处理 {len(html_files)} 个HTML文件...\n")
    print("=" * 80)
    
    articles_with_images = []
    all_images = {}
    
    # 第一步：收集所有图片信息
    for html_file in html_files:
        result = get_images_from_html(html_file)
        if result and result['images']:
            articles_with_images.append(result)
            for img in result['images']:
                all_images[img['filename']] = img
    
    print(f"找到 {len(articles_with_images)} 篇包含图片的文章")
    print(f"总共 {len(all_images)} 张不同的图片\n")
    
    # 第二步：复制所有图片到图床
    print("=" * 80)
    print("上传图片到图床:")
    print("=" * 80)
    
    for filename in sorted(all_images.keys()):
        copy_image_file(filename)
    
    # 第三步：更新文章
    print("\n" + "=" * 80)
    print("更新文章引用:")
    print("=" * 80)
    
    updated_count = 0
    for article_info in articles_with_images:
        md_file = find_article_file(article_info['title'], article_info['published'])
        if md_file:
            count = add_images_to_article(md_file, article_info['images'])
            if count:
                print(f"\n✓ {md_file.name}")
                print(f"  已添加 {count} 张图片")
                for img in article_info['images']:
                    if img['filename'] not in open(md_file).read():
                        continue
                    print(f"    - {img['filename']}")
                updated_count += 1
        else:
            print(f"\n✗ 未找到对应的Markdown文件: {article_info['title']}")
    
    print("\n" + "=" * 80)
    print(f"✅ 完成！已更新 {updated_count} 篇文章")
    print("=" * 80)

if __name__ == '__main__':
    main()
