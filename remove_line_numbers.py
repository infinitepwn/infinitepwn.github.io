#!/usr/bin/env python3
"""
删除代码块中的纯数字行（作为行号）
"""

import re
from pathlib import Path

def remove_standalone_line_numbers(content):
    """删除代码块中的独立数字行"""
    
    def clean_code_block(match):
        lang = match.group(1) or ''
        code = match.group(2) or ''
        
        lines = code.split('\n')
        # 删除仅包含 1-99 数字的行
        cleaned = []
        for line in lines:
            # 如果行只包含数字（1-99），跳过
            if re.match(r'^\d{1,2}$', line.strip()):
                continue
            cleaned.append(line)
        
        result_code = '\n'.join(cleaned)
        return '```' + lang + '\n' + result_code + '\n```'
    
    # 处理所有代码块
    pattern = r'```([a-zA-Z0-9_+-]*)\n(.*?)\n```'
    result = re.sub(pattern, clean_code_block, content, flags=re.DOTALL)
    
    return result

# 处理所有文章
posts_dir = Path('/Users/infinite/Documents/blog/source/_posts')
fixed = []

for md_file in sorted(posts_dir.glob('*.md')):
    with open(md_file, 'r', encoding='utf-8') as f:
        original = f.read()
    
    modified = remove_standalone_line_numbers(original)
    
    if modified != original:
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(modified)
        fixed.append(md_file.name)
        print(f"✅ {md_file.name}")

print(f"\n修复 {len(fixed)} 篇文章")
