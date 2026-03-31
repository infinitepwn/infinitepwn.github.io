#!/usr/bin/env python3
"""
转换 LaTeX 公式格式：
\[...\] → $$...$$
\(...\) → $...$
"""

import re
from pathlib import Path

def convert_latex_format(content):
    """转换LaTeX公式格式"""
    
    # 先处理代码块，暂时存储它们
    code_blocks = []
    def store_code(match):
        code_blocks.append(match.group(0))
        return f"__CODE_BLOCK_{len(code_blocks)-1}__"
    
    content = re.sub(r'```[^`]*```', store_code, content, flags=re.DOTALL)
    
    # 转换 \[ ... \] 为 $$ ... $$（显示模式）
    content = re.sub(r'\\\[(.*?)\\\]', r'$$\1$$', content, flags=re.DOTALL)
    
    # 转换 \( ... \) 为 $ ... $（行内模式）
    content = re.sub(r'\\\((.*?)\\\)', r'$\1$', content, flags=re.DOTALL)
    
    # 恢复代码块
    for i, block in enumerate(code_blocks):
        content = content.replace(f"__CODE_BLOCK_{i}__", block)
    
    return content

# 处理所有文章
posts_dir = Path('/Users/infinite/Documents/blog/source/_posts')
converted = 0

for md_file in sorted(posts_dir.glob('*.md')):
    with open(md_file, 'r', encoding='utf-8') as f:
        original = f.read()
    
    modified = convert_latex_format(original)
    
    if modified != original:
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(modified)
        converted += 1
        if '公式' in original or '\\[' in original or '$' in original:
            print(f"✅ {md_file.name}")

print(f"\n转换 {converted} 篇文章的公式格式")
