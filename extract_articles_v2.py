#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用BeautifulSoup从Hexo HTML文件提取完整文章
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("Installing beautifulsoup4...")
    os.system("pip install beautifulsoup4 -q")
    from bs4 import BeautifulSoup

def extract_code_blocks(element):
    """从figure标签中提取代码块"""
    result = []
    for fig in element.find_all('figure', class_='highlight'):
        # 获取语言
        lang_match = re.search(r'highlight["\s]+(\w+)', str(fig.get('class', '')))
        lang = ''
        
        # 从代码行提取内容
        lines = []
        for span in fig.find_all('span', class_='line'):
            # 获取纯文本
            line_text = span.get_text()
            lines.append(line_text)
        
        if lines:
            code_text = '\n'.join(lines)
            result.append(f'```{lang}\n{code_text}\n```\n\n')
    
    return result

def convert_html_to_markdown(html_element):
    """将BeautifulSoup元素转换为Markdown"""
    markdown = []
    
    for element in html_element.children:
        if isinstance(element, str):
            text = str(element).strip()
            if text:
                markdown.append(text)
        else:
            tag_name = element.name
            
            if tag_name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                level = int(tag_name[1])
                text = element.get_text()
                markdown.append(f"{'#' * level} {text}\n")
            
            elif tag_name == 'p':
                text = element.get_text()
                if text.strip():
                    markdown.append(f"{text}\n\n")
            
            elif tag_name == 'figure' and 'highlight' in element.get('class', []):
                # 处理代码块
                lang = ''
                class_str = ' '.join(element.get('class', []))
                lang_match = re.search(r'highlight-(\w+)', class_str)
                if lang_match:
                    lang = lang_match.group(1)
                
                lines = []
                for span in element.find_all('span', class_='line'):
                    line_text = span.get_text()
                    lines.append(line_text)
                
                if lines:
                    code = '\n'.join(lines)
                    markdown.append(f'```{lang}\n{code}\n```\n\n')
            
            elif tag_name == 'code':
                markdown.append(f"`{element.get_text()}`")
            
            elif tag_name in ['strong', 'b']:
                markdown.append(f"**{element.get_text()}**")
            
            elif tag_name in ['em', 'i']:
                markdown.append(f"*{element.get_text()}*")
            
            elif tag_name == 'a':
                href = element.get('href', '#')
                text = element.get_text()
                markdown.append(f"[{text}]({href})")
            
            elif tag_name == 'ul':
                for li in element.find_all('li', recursive=False):
                    markdown.append(f"- {li.get_text()}\n")
            
            elif tag_name == 'ol':
                for i, li in enumerate(element.find_all('li', recursive=False), 1):
                    markdown.append(f"{i}. {li.get_text()}\n")
            
            elif tag_name == 'br':
                markdown.append("\n")
            
            elif tag_name == 'table':
                # 简单的表格处理
                markdown.append(element.get_text() + "\n\n")
            
            else:
                # 递归处理其他元素
                inner = convert_html_to_markdown(element)
                if inner:
                    markdown.append(inner)
    
    return ''.join(markdown)

def process_html_file(html_path):
    """处理单个HTML文件"""
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
        
        # 提取元数据
        title_tag = soup.find('meta', property='og:title')
        title = title_tag.get('content', '无标题') if title_tag else '无标题'
        
        published_tag = soup.find('meta', property='article:published_time')
        published = published_tag.get('content', '') if published_tag else ''
        
        # 提取所有标签
        tags = []
        for tag_elem in soup.find_all('meta', property='article:tag'):
            tags.append(tag_elem.get('content', ''))
        
        # 提取文章正文
        article = soup.find('article', class_='post-content')
        if not article:
            return None
        
        # 转换为Markdown
        markdown_content = convert_html_to_markdown(article)
        
        # 清理多余空行
        markdown_content = re.sub(r'\n\n\n+', '\n\n', markdown_content)
        markdown_content = markdown_content.strip()
        
        # 构建Front Matter
        date_str = ''
        if published:
            try:
                dt = datetime.fromisoformat(published.replace('Z', '+00:00'))
                date_str = dt.strftime('%Y-%m-%d %H:%M:%S')
            except:
                date_str = published
        
        tags_json = json.dumps(tags) if tags else '[]'
        
        front_matter = f"""---
title: {title}
date: {date_str}
tags: {tags_json}
---

"""
        full_content = front_matter + markdown_content
        
        return {
            'title': title,
            'content': full_content,
            'published': published
        }
    
    except Exception as e:
        print(f"Error: {e}")
        return None

def main():
    backup_dir = Path(os.path.expanduser('~/Documents/blog-backup/post'))
    output_dir = Path(os.path.expanduser('~/Documents/blog/source/_posts_recovered_v2'))
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    html_files = sorted(backup_dir.glob('*.html'))
    print(f"Found {len(html_files)} HTML files\n")
    
    success_count = 0
    for i, html_file in enumerate(html_files, 1):
        result = process_html_file(str(html_file))
        
        if result:
            # 生成文件名
            title = result['title']
            published = result['published']
            
            # 使用发布日期作为前缀
            if published:
                try:
                    dt = datetime.fromisoformat(published.replace('Z', '+00:00'))
                    date_prefix = dt.strftime('%Y-%m-%d')
                except:
                    date_prefix = ''
            else:
                date_prefix = ''
            
            # 清理标题作为文件名
            clean_title = re.sub(r'[^\w\u4e00-\u9fff\s-]', '', title)
            clean_title = re.sub(r'\s+', '-', clean_title.strip())[:50]
            
            if date_prefix:
                filename = f"{date_prefix}_{clean_title}.md"
            else:
                filename = f"{clean_title}.md"
            
            output_file = output_dir / filename
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(result['content'])
            
            print(f"[{i}/{len(html_files)}] ✓ {title[:40]:<40} → {filename}")
            success_count += 1
        else:
            print(f"[{i}/{len(html_files)}] ✗ {html_file.name}")
    
    print(f"\n成功提取 {success_count}/{len(html_files)} 篇文章")
    print(f"输出目录: {output_dir}")

if __name__ == '__main__':
    main()
