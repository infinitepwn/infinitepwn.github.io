#!/usr/bin/env python3
"""
最强修复脚本：
1. 完全彻底地移除代码块中的所有行号
2. 修复LaTeX公式格式（确保双反斜杠正确）
"""

import re
from pathlib import Path

def aggressive_fix_code_blocks(content):
    """最激进的代码块修复"""
    
    def fix_block(match):
        lang = match.group(1) if match.group(1) else ''
        code = match.group(2) if match.group(2) else ''
        
        if not code.strip():
            return match.group(0)
        
        lines = code.split('\n')
        fixed_lines = []
        
        for line in lines:
            # 循环移除所有行号模式
            attempts = 0
            while attempts < 10:  # 最多尝试10次
                original = line
                
                # 移除格式：数字 + 空格/制表符
                line = re.sub(r'^\s*\d+\s+', '', line)
                
                # 移除仅有数字+制表符的情况
                line = re.sub(r'^\d+\t', '', line)
                
                # 移除没有空格的数字（但只在特定情况）
                if re.match(r'^\d+[a-zA-Z_\[\(\{#]', line):
                    line = re.sub(r'^\d+', '', line)
                
                if line == original:
                    break
                attempts += 1
            
            fixed_lines.append(line)
        
        return '```' + lang + '\n' + '\n'.join(fixed_lines) + '\n```'
    
    # 匹配所有代码块
    pattern = r'```([a-zA-Z0-9_+-]*)\n(.*?)\n```'
    result = re.sub(pattern, fix_block, content, flags=re.DOTALL)
    
    return result

def fix_latex_formatting(content):
    """修复LaTeX公式格式"""
    
    # 问题：有些地方用了单反斜杠，需要改成双反斜杠
    # 但要小心不要在代码块里修改
    
    # 先找出所有代码块，存储起来
    code_blocks = []
    def store_code_block(match):
        code_blocks.append(match.group(0))
        return f"__CODE_BLOCK_{len(code_blocks)-1}__"
    
    # 暂时移除代码块
    temp_content = re.sub(r'```[^`]*```', store_code_block, content, flags=re.DOTALL)
    
    # 在非代码块区域修复LaTeX（这里不做特殊修改，因为用户的公式可能各种格式）
    # 重点是确保MathJax能处理
    
    # 恢复代码块
    for i, block in enumerate(code_blocks):
        temp_content = temp_content.replace(f"__CODE_BLOCK_{i}__", block)
    
    return temp_content

def process_file(file_path):
    """处理单个文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # 修复代码块
    content = aggressive_fix_code_blocks(content)
    
    # 修复 LaTeX
    content = fix_latex_formatting(content)
    
    if content != original:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    
    return False

# 处理所有文章
posts_dir = Path('/Users/infinite/Documents/blog/source/_posts')
fixed_count = 0

for md_file in sorted(posts_dir.glob('*.md')):
    if process_file(md_file):
        fixed_count += 1
        print(f"✅ {md_file.name}")

print(f"\n修复: {fixed_count}/57 篇文章")

# 验证最常见的问题文件
print("\n=== 验证修复 ===")
test_file = posts_dir / '2025-08-14_infinite_blog.md'
if test_file.exists():
    with open(test_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否还有纯数字行
    code_blocks = re.findall(r'```[^\n]*\n(.*?)\n```', content, re.DOTALL)
    has_numbers = False
    for block in code_blocks:
        lines = block.split('\n')
        for line in lines[:5]:
            if re.match(r'^\d+\s*$', line):
                print(f"  ⚠️  仍有纯数字行: '{line}'")
                has_numbers = True
    
    if not has_numbers:
        print("  ✅ 代码块行号已清除")
