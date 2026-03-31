#!/usr/bin/env python3
"""
修复所有文章的问题：
1. 移除代码块中的行号前缀
2. 启用LaTeX公式渲染支持
"""

import os
import re
from pathlib import Path

def fix_code_blocks_in_content(content):
    """移除代码块中的行号前缀"""
    # 匹配所有代码块 (支持多行)
    pattern = r'```(.*?)\n(.*?)\n```'
    
    def remove_line_numbers(match):
        lang = match.group(1)  # 编程语言标签 (如 python, bash 等)
        code_block = match.group(2)
        
        # 处理代码块中的每一行
        lines = code_block.split('\n')
        fixed_lines = []
        
        for line in lines:
            # 移除开头的行号及其后面的空格或制表符
            # 匹配模式：一个或多个数字 + 可选的空格/制表符 + 剩余内容
            fixed_line = re.sub(r'^\d+\s+', '', line)
            fixed_lines.append(fixed_line)
        
        return '```' + lang + '\n' + '\n'.join(fixed_lines) + '\n```'
    
    # 使用 DOTALL 标志使 . 能匹配换行符
    fixed_content = re.sub(pattern, remove_line_numbers, content, flags=re.DOTALL)
    return fixed_content

def add_latex_support(content):
    """
    在 Front Matter 中添加 LaTeX 支持
    如果已有 mathjax 标签，则不添加
    """
    # 检查是否已有 mathjax 标签
    if 'mathjax' in content.lower():
        return content
    
    # 找到 Front Matter 的结束位置
    if content.startswith('---'):
        # 找第二个 --- 的位置
        first_close = content.find('---', 3)
        if first_close != -1:
            front_matter = content[:first_close]
            rest = content[first_close:]
            
            # 在 Front Matter 末尾添加 mathjax: true
            if not rest.startswith('---\n'):
                rest = '---\n' + rest[3:]
            
            # 检查是否需要添加 mathjax 标签
            if 'mathjax' not in front_matter:
                # 在最后一个标签前添加 mathjax
                front_matter = front_matter.rstrip() + '\nmathjax: true\n'
            
            return front_matter + rest
    
    return content

def process_file(file_path):
    """处理单个 Markdown 文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # 修复代码块
    content = fix_code_blocks_in_content(content)
    
    # 添加 LaTeX 支持
    content = add_latex_support(content)
    
    # 只有内容改变时才写回文件
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    
    return False

# 处理所有 Markdown 文件
posts_dir = Path('/Users/infinite/Documents/blog/source/_posts')
fixed_count = 0
total_count = 0

for md_file in sorted(posts_dir.glob('*.md')):
    total_count += 1
    try:
        if process_file(md_file):
            fixed_count += 1
            print(f"✅ {md_file.name}")
    except Exception as e:
        print(f"❌ {md_file.name}: {e}")

print(f"\n{'='*60}")
print(f"总共处理: {total_count} 篇文章")
print(f"修复: {fixed_count} 篇文章")
print(f"{'='*60}")
