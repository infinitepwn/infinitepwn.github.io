#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从已发布的 HTML 文件中提取文章内容，转换为 Markdown
"""

import os
import re
import json
from pathlib import Path
from html import unescape
from datetime import datetime

def extract_metadata_from_html(html_file):
    """从 HTML 中提取元数据"""
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取 JSON-LD 数据
        json_ld_match = re.search(r'<script type="application/ld\+json">(.*?)</script>', content, re.DOTALL)
        if json_ld_match:
            try:
                json_data = json.loads(json_ld_match.group(1))
                title = json_data.get('headline', '无标题')
                date_published = json_data.get('datePublished', '')
                
                # 解析日期
                try:
                    date_obj = datetime.fromisoformat(date_published.replace('Z', '+00:00'))
                    date_str = date_obj.strftime('%Y-%m-%d %H:%M:%S')
                except:
                    date_str = date_published
                
                return {
                    'title': title,
                    'date': date_str,
                    'filename': Path(html_file).stem
                }
            except json.JSONDecodeError:
                pass
        
        # 备用方案：从 meta 标签提取
        title_match = re.search(r'<meta property="og:title" content="([^"]*)"', content)
        date_match = re.search(r'<meta property="article:published_time" content="([^"]*)"', content)
        
        title = title_match.group(1) if title_match else '无标题'
        date_published = date_match.group(1) if date_match else ''
        
        try:
            date_obj = datetime.fromisoformat(date_published.replace('Z', '+00:00'))
            date_str = date_obj.strftime('%Y-%m-%d %H:%M:%S')
        except:
            date_str = date_published
        
        return {
            'title': unescape(title),
            'date': date_str,
            'filename': Path(html_file).stem
        }
    except Exception as e:
        print(f"❌ 处理 {html_file} 时出错: {e}")
        return None

def extract_content_from_html(html_file):
    """从 HTML 中提取文章内容（简化版）"""
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 查找文章内容（通常在 <article> 或特定 class 中）
        # 这是一个简化的提取，可能需要根据实际主题调整
        
        # 尝试找到 <article> 标签中的内容
        article_match = re.search(r'<article[^>]*>(.*?)</article>', content, re.DOTALL)
        
        if article_match:
            article_html = article_match.group(1)
            # 移除脚本和样式标签
            article_html = re.sub(r'<script[^>]*>.*?</script>', '', article_html, flags=re.DOTALL)
            article_html = re.sub(r'<style[^>]*>.*?</style>', '', article_html, flags=re.DOTALL)
            
            # 简单的 HTML 到文本的转换
            text = re.sub(r'<[^>]+>', '', article_html)
            text = unescape(text)
            text = re.sub(r'\s+', ' ', text).strip()
            
            return text[:500]  # 返回前 500 个字符
        
        return "无法提取内容"
    except Exception as e:
        print(f"❌ 提取内容失败: {e}")
        return "无法提取内容"

def generate_markdown_from_html(html_dir, output_dir):
    """批量转换 HTML 为 Markdown"""
    
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    html_files = sorted(Path(html_dir).glob('*.html'))
    print(f"📊 找到 {len(html_files)} 个 HTML 文件\n")
    
    successful = 0
    
    for i, html_file in enumerate(html_files, 1):
        metadata = extract_metadata_from_html(str(html_file))
        if not metadata:
            continue
        
        title = metadata['title']
        date = metadata['date']
        filename = metadata['filename']
        
        # 生成安全的文件名
        safe_filename = re.sub(r'[^\w\-]', '_', title)[:50]
        md_filename = f"{safe_filename}.md"
        md_path = Path(output_dir) / md_filename
        
        # 避免文件名冲突
        counter = 1
        base_path = md_path
        while md_path.exists():
            md_path = Path(output_dir) / f"{safe_filename}_{counter}.md"
            counter += 1
        
        # 创建 Markdown 内容
        markdown_content = f"""---
title: {title}
date: {date}
categories:
  - 未分类
tags:
  - 导入
---

<!-- 本文是从已发布的 HTML 逆向提取的内容 -->
<!-- 原始文件: {filename}.html -->

> ⚠️ 注意: 这是自动从 HTML 提取的内容，可能需要手动调整格式

## 内容预览

{extract_content_from_html(str(html_file))}

...

*更多内容需要手动补充*

"""
        
        try:
            md_path.write_text(markdown_content, encoding='utf-8')
            print(f"✅ [{i}/{len(html_files)}] {title}")
            successful += 1
        except Exception as e:
            print(f"❌ [{i}/{len(html_files)}] 写入失败: {e}")
    
    print(f"\n✨ 成功生成 {successful}/{len(html_files)} 个 Markdown 文件")
    print(f"📁 文件保存在: {output_dir}")

if __name__ == '__main__':
    html_source = os.path.expanduser('~/Documents/blog-backup/post')
    markdown_output = os.path.expanduser('~/Documents/blog/source/_posts_recovered')
    
    print("🔄 开始从 HTML 提取文章内容...\n")
    generate_markdown_from_html(html_source, markdown_output)
    print("\n✅ 完成！请检查生成的文件并手动调整内容。")
