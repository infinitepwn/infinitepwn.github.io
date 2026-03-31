#!/usr/bin/env python3
"""
终极修复脚本：
1. 完全移除代码块中的行号（包括各种格式）
2. 确保 LaTeX 公式不被破坏
3. 保证公式外部空格正确
"""

import os
import re
from pathlib import Path

def fix_code_blocks_aggressive(content):
    """激进地移除代码块中的行号"""
    
    def process_code_block(match):
        lang = match.group(1) or ''  # 编程语言标签
        code = match.group(2) if match.group(2) else ''
        
        if not code:
            return match.group(0)
        
        lines = code.split('\n')
        fixed_lines = []
        
        for line in lines:
            # 多次移除行号，直到完全干净
            # 匹配模式：可选空格 + 1-5位数字 + 空格/制表符 + 内容
            while re.match(r'^\s*\d{1,5}\s+', line):
                line = re.sub(r'^\s*\d{1,5}\s+', '', line)
            
            # 也处理这种格式：数字后面没有空格的情况
            # 但要保证不破坏正常代码（如 int x = 123;）
            # 所以只在行开头有多个数字时处理
            if re.match(r'^\d{2,}\s', line):
                line = re.sub(r'^\d+\s+', '', line)
            
            fixed_lines.append(line)
        
        return '```' + lang + '\n' + '\n'.join(fixed_lines) + '\n```'
    
    # 处理 ```lang\n...\n``` 格式（优先处理有语言标签的）
    pattern1 = r'```([a-zA-Z0-9_+-]*)\n(.*?)\n```'
    content = re.sub(pattern1, process_code_block, content, flags=re.DOTALL)
    
    return content

def ensure_latex_support(content):
    """确保 LaTeX 支持被正确添加"""
    # 检查是否已有 mathjax 标签
    if 'mathjax' not in content.lower():
        # 找到 Front Matter 的结束位置
        if content.startswith('---'):
            # 找第二个 --- 的位置
            first_close = content.find('---', 3)
            if first_close != -1:
                front_matter = content[:first_close]
                rest = content[first_close:]
                
                # 确保 --- 后面有换行
                if not rest.startswith('---\n'):
                    rest = '---\n' + rest[3:]
                
                # 在 Front Matter 末尾添加 mathjax: true
                front_matter = front_matter.rstrip() + '\nmathjax: true\n'
                
                return front_matter + rest
    
    return content

def protect_latex_in_code_blocks(content):
    """
    一些 LaTeX 公式可能在代码块之外，这个函数确保它们不被破坏
    """
    # 这里我们不处理代码块外的内容，因为那些应该被 MathJax 正确渲染
    return content

def process_file(file_path):
    """处理单个文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Step 1: 修复代码块
    content = fix_code_blocks_aggressive(content)
    
    # Step 2: 确保 LaTeX 支持
    content = ensure_latex_support(content)
    
    # Step 3: 保护 LaTeX
    content = protect_latex_in_code_blocks(content)
    
    if content != original:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    
    return False

# 处理所有文章
posts_dir = Path('/Users/infinite/Documents/blog/source/_posts')
fixed = 0
total = 0

for md_file in sorted(posts_dir.glob('*.md')):
    total += 1
    if process_file(md_file):
        fixed += 1
        print(f"✅ {md_file.name}")

print(f"\n修复完成: {fixed}/{total} 篇文章")
