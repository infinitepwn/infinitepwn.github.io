#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从HTML备份中提取所有CDN图片引用并添加到Markdown文章
"""

import re
from pathlib import Path
from bs4 import BeautifulSoup
from datetime import datetime

CDN_BASE = "https://raw.githubusercontent.com/infinitepwn/blogimage/main"
HTML_BACKUP_DIR = Path("/Users/infinite/Documents/blog-backup/post")
POSTS_DIR = Path("/Users/infinite/Documents/blog/source/_posts")

def extract_cdn_images(html_file):
    """从HTML中提取CDN图片和文章信息"""
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
        
        # 获取文章信息
        title_tag = soup.find('meta', property='og:title')
        title = title_tag.get('content', '') if title_tag else ''
        
        published_tag = soup.find('meta', property='article:published_time')
        published = published_tag.get('content', '') if published_tag else ''
        
        # 提取文章内容中的所有img标签
        images = []
        article = soup.find('article', class_='post-content')
        if article:
            for img in article.find_all('img'):
                src = img.get('src', '')
                alt = img.get('alt', 'image')
                
                # 提取图片文件名
                if src:
                    # 如果是CDN链接，提取文件名
                    if 'cdn.jsdelivr.net' in src or 'github' in src:
                        # 从CDN URL中提取文件名
                        filename = src.split('/')[-1]
                        images.append({
                            'src': src,
                            'alt': alt,
                            'filename': filename
                        })
                    # 如果是相对路径，也提取
                    elif src.startswith('/') and '/' in src[1:]:
                        if not any(x in src for x in ['img/head', '/js/', '/css/', '/api/']):
                            filename = src.split('/')[-1]
                            images.append({
                                'src': src,
                                'alt': alt,
                                'filename': filename
                            })
        
        return {
            'title': title,
            'published': published,
            'images': images
        }
    except Exception as e:
        print(f"Error reading {html_file}: {e}")
        return None

def find_md_file(title, published):
    """根据标题和日期查找Markdown文件"""
    if published:
        try:
            # 提取日期前缀
            date_prefix = published.split('T')[0]
            # 查找匹配的文件
            matches = list(POSTS_DIR.glob(f"{date_prefix}_*.md"))
            if matches:
                return matches[0]
        except:
            pass
    
    # 模糊匹配标题
    clean_title = re.sub(r'[^\w\u4e00-\u9fff\s-]', '', title)
    for md_file in POSTS_DIR.glob('*.md'):
        if clean_title.lower() in md_file.name.lower():
            return md_file
    
    return None

def add_cdn_images_to_article(md_file, images):
    """添加CDN图片到文章"""
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 过滤出还不在文章中的图片
    new_images = []
    for img in images:
        # 检查是否已存在
        if img['filename'] not in content:
            new_images.append(img)
    
    if not new_images:
        return 0
    
    # 构建图片markdown
    img_md = ''
    for img in new_images:
        # 如果是相对路径，转换为CDN
        if img['src'].startswith('/'):
            cdn_url = f"{CDN_BASE}/{img['filename']}"
        else:
            cdn_url = img['src']
        
        img_md += f"![{img['alt']}]({cdn_url})\n\n"
    
    # 在Front Matter后添加
    parts = content.split('---', 2)
    if len(parts) == 3:
        new_content = '---' + parts[1] + '---\n\n' + img_md + parts[2]
    else:
        new_content = img_md + content
    
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return len(new_images)

def main():
    html_files = sorted(HTML_BACKUP_DIR.glob('*.html'))
    
    print(f"处理 {len(html_files)} 个HTML文件...\n")
    
    articles_data = []
    
    # 收集所有文章数据
    for html_file in html_files:
        result = extract_cdn_images(html_file)
        if result and result['images']:
            articles_data.append(result)
    
    print(f"找到 {len(articles_data)} 篇包含图片的文章\n")
    
    if not articles_data:
        print("没有找到任何图片")
        return
    
    print("=" * 80)
    print("更新文章图片引用:")
    print("=" * 80)
    
    updated_count = 0
    total_images = 0
    
    for article in articles_data:
        md_file = find_md_file(article['title'], article['published'])
        
        if md_file:
            count = add_cdn_images_to_article(md_file, article['images'])
            if count > 0:
                print(f"\n✓ {md_file.name}")
                print(f"  已添加 {count} 张图片:")
                for img in article['images']:
                    if img['filename'] not in open(md_file).read():
                        continue
                    print(f"    - {img['filename']}")
                updated_count += 1
                total_images += count
        else:
            print(f"\n⊘ 未找到对应文件: {article['title']}")
    
    print("\n" + "=" * 80)
    print(f"✅ 完成！已更新 {updated_count} 篇文章，共添加 {total_images} 张图片")
    print("=" * 80)

if __name__ == '__main__':
    main()
