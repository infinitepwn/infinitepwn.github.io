#!/usr/bin/env python3
"""修复代码块中的行号问题"""

import os
import re
from pathlib import Path

def fix_code_blocks(file_path):
    """移除代码块中的行号前缀"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 找到所有代码块
    pattern = r'```\n(.*?)\n```'
    
    def remove_line_numbers(match):
        code_block = match.group(1)
        # 移除每行开头的行号（1, 2, 3 等）
        lines = code_block.split('\n')
        fixed_lines = []
        
        for line in lines:
            # 移除开头的行号及其后面的空格
            # 匹配模式：一个或多个数字 + 可选空格 + 剩余内容
            fixed_line = re.sub(r'^(\d+)\s*', '', line)
            fixed_lines.append(fixed_line)
        
        return '```\n' + '\n'.join(fixed_lines) + '\n```'
    
    fixed_content = re.sub(pattern, remove_line_numbers, content, flags=re.DOTALL)
    
    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    
    return True

# 处理有问题的三个文件
problem_files = [
    '/Users/infinite/Documents/blog/source/_posts/2025-01-17_春秋GAME-WP.md',
    '/Users/infinite/Documents/blog/source/_posts/2025-05-30_z3的使用.md',
    '/Users/infinite/Documents/blog/source/_posts/2025-07-09_哈希长度拓展攻击.md'
]

for file_path in problem_files:
    if os.path.exists(file_path):
        try:
            fix_code_blocks(file_path)
            print(f"✅ 已修复: {Path(file_path).name}")
        except Exception as e:
            print(f"❌ 修复失败: {Path(file_path).name} - {e}")
    else:
        print(f"⚠️  文件不存在: {file_path}")

print("\n✅ 代码块修复完成！")
