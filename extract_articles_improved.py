#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从Hexo生成的HTML文件提取完整文章内容并转换为Markdown
"""

import os
import re
from pathlib import Path
from html.parser import HTMLParser
from html import unescape
import json
from datetime import datetime

class ArticleExtractor(HTMLParser):
    """从HTML中提取文章内容的解析器"""
    
    def __init__(self):
        super().__init__()
        self.in_article = False
        self.in_code = False
        self.article_html = []
        self.metadata = {}
        self.collecting = False
        
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        
        # 收集元数据
        if tag == 'meta':
            if attrs_dict.get('property') == 'og:title':
                self.metadata['title'] = attrs_dict.get('content', '')
            elif attrs_dict.get('property') == 'og:description':
                self.metadata['description'] = attrs_dict.get('content', '')
            elif attrs_dict.get('property') == 'article:published_time':
                self.metadata['published'] = attrs_dict.get('content', '')
            elif attrs_dict.get('property') == 'article:tag':
                if 'tags' not in self.metadata:
                    self.metadata['tags'] = []
                self.metadata['tags'].append(attrs_dict.get('content', ''))
        
        # 检测文章容器开始
        if tag == 'article' and 'article-container' in attrs_dict.get('class', ''):
            self.in_article = True
            self.collecting = True
            
        if self.in_article:
            self.article_html.append(f"<{tag}{''.join(f' {k}=\"{v}\"' for k, v in attrs)}>")
    
    def handle_endtag(self, tag):
        if self.in_article:
            self.article_html.append(f"</{tag}>")
            
            if tag == 'article':
                self.in_article = False
                self.collecting = False
    
    def handle_data(self, data):
        if self.in_article and self.collecting:
            self.article_html.append(data)
    
    def get_article_html(self):
        return ''.join(self.article_html)

def html_to_markdown(html_content):
    """将HTML转换为Markdown"""
    markdown = html_content
    
    # 处理标题
    markdown = re.sub(r'<h1[^>]*>(.*?)</h1>', r'# \1', markdown)
    markdown = re.sub(r'<h2[^>]*>(.*?)</h2>', r'## \1', markdown)
    markdown = re.sub(r'<h3[^>]*>(.*?)</h3>', r'### \1', markdown)
    markdown = re.sub(r'<h4[^>]*>(.*?)</h4>', r'#### \1', markdown)
    markdown = re.sub(r'<h5[^>]*>(.*?)</h5>', r'##### \1', markdown)
    markdown = re.sub(r'<h6[^>]*>(.*?)</h6>', r'###### \1', markdown)
    
    # 处理段落
    markdown = re.sub(r'<p[^>]*>(.*?)</p>', r'\1\n\n', markdown, flags=re.DOTALL)
    
    # 处理代码块
    markdown = re.sub(r'<figure class="highlight[^"]*">(.*?)</figure>', lambda m: extract_code_block(m.group(1)), markdown, flags=re.DOTALL)
    markdown = re.sub(r'<code[^>]*>(.*?)</code>', r'`\1`', markdown)
    
    # 处理加粗和斜体
    markdown = re.sub(r'<strong[^>]*>(.*?)</strong>', r'**\1**', markdown)
    markdown = re.sub(r'<em[^>]*>(.*?)</em>', r'*\1*', markdown)
    markdown = re.sub(r'<b[^>]*>(.*?)</b>', r'**\1**', markdown)
    markdown = re.sub(r'<i[^>]*>(.*?)</i>', r'*\1*', markdown)
    
    # 处理链接
    markdown = re.sub(r'<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>', r'[\2](\1)', markdown)
    
    # 处理列表
    markdown = re.sub(r'<li[^>]*>(.*?)</li>', r'- \1\n', markdown, flags=re.DOTALL)
    markdown = re.sub(r'<ul[^>]*>(.*?)</ul>', r'\1', markdown, flags=re.DOTALL)
    markdown = re.sub(r'<ol[^>]*>(.*?)</ol>', r'\1', markdown, flags=re.DOTALL)
    
    # 处理换行
    markdown = re.sub(r'<br\s*/?>', '\n', markdown)
    markdown = re.sub(r'<hr\s*/?>', '\n---\n', markdown)
    
    # 清理HTML实体
    markdown = unescape(markdown)
    
    # 清理多余的HTML标签
    markdown = re.sub(r'<[^>]+>', '', markdown)
    
    # 清理多余空行
    markdown = re.sub(r'\n\n\n+', '\n\n', markdown)
    markdown = markdown.strip()
    
    return markdown

def extract_code_block(html_content):
    """从figure元素中提取代码内容"""
    # 移除table和其他包装
    lines = []
    in_code = False
    
    for match in re.finditer(r'<span class="line">(.*?)</span>', html_content):
        line = match.group(1)
        line = re.sub(r'<span[^>]*>', '', line)
        line = re.sub(r'</span>', '', line)
        line = unescape(line)
        line = re.sub(r'<br\s*/?>', '', line)
        lines.append(line)
    
    if lines:
        code = '\n'.join(lines)
        # 尝试检测语言
        lang = re.search(r'highlight["\s]+(\w+)', html_content)
        lang_name = lang.group(1) if lang else ''
        return f'```{lang_name}\n{code}\n```\n\n'
    
    return ''

def process_html_file(html_path):
    """处理单个HTML文件"""
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # 提取元数据和正文
        extractor = ArticleExtractor()
        extractor.feed(html_content)
        
        metadata = extractor.metadata
        article_html = extractor.get_article_html()
        
        if not metadata.get('title'):
            return None
        
        # 转换为Markdown
        markdown_content = html_to_markdown(article_html)
        
        # 构建Front Matter
        title = metadata.get('title', '无标题')
        published = metadata.get('published', '')
        tags = metadata.get('tags', [])
        
        # 解析日期
        date_str = ''
        if published:
            try:
                dt = datetime.fromisoformat(published.replace('Z', '+00:00'))
                date_str = dt.strftime('%Y-%m-%d %H:%M:%S')
            except:
                date_str = published
        
        # 构建Markdown文件内容
        front_matter = f"""---
title: {title}
date: {date_str}
tags: {json.dumps(tags)}
---

"""
        full_content = front_matter + markdown_content
        
        return {
            'title': title,
            'content': full_content,
            'published': published
        }
    
    except Exception as e:
        print(f"Error processing {html_path}: {e}")
        return None

def main():
    backup_dir = Path(os.path.expanduser('~/Documents/blog-backup/post'))
    output_dir = Path(os.path.expanduser('~/Documents/blog/source/_posts_recovered'))
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    html_files = sorted(backup_dir.glob('*.html'))
    print(f"Found {len(html_files)} HTML files")
    
    success_count = 0
    for html_file in html_files:
        result = process_html_file(str(html_file))
        
        if result:
            # 使用发布日期和标题生成文件名
            published = result['published']
            title = result['title']
            
            # 生成简洁的文件名
            filename = f"{title.lower().replace(' ', '-')}.md"
            filename = re.sub(r'[^\w\-]', '', filename)[:50] + '.md'
            if not filename or filename == '.md':
                filename = html_file.stem + '.md'
            
            output_file = output_dir / filename
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(result['content'])
            
            print(f"✓ {filename}")
            success_count += 1
        else:
            print(f"✗ Skipped {html_file.name}")
    
    print(f"\n成功提取 {success_count} 篇文章到 {output_dir}")

if __name__ == '__main__':
    main()
