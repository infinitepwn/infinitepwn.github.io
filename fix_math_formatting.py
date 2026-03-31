#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

markdown_file = "/Users/infinite/Documents/blog/source/_posts/2024-12-20_微分方程.md"

with open(markdown_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 问题：许多行以\ 开头或包含\\ 但没有被$$包裹
# 策略：找到所有这样的行，为它们添加$$

# 分行处理
lines = content.split('\n')
output = []
in_math_block = False

i = 0
while i < len(lines):
    line = lines[i]
    
    # 检查是否是LaTeX行
    has_latex = bool(re.search(r'\\\w|\\\\', line))
    is_comment = line.strip().startswith('#')
    is_empty = not line.strip()
    is_code = line.strip().startswith('```')
    
    if has_latex and not is_comment and not is_empty and not is_code:
        # 这是一个需要格式化的行
        
        # 检查是否已有$$
        if '$$' in line:
            # 已经有$$，保持原样
            output.append(line)
            in_math_block = False
        else:
            # 需要添加$$
            # 检查当前是否在数学块中
            if not in_math_block:
                output.append('$$')
                in_math_block = True
            
            output.append(line)
            
            # 检查这一行是否应该结束数学块
            # 如果下一行不是LaTeX行，则结束
            if i + 1 < len(lines):
                next_line = lines[i + 1]
                next_has_latex = bool(re.search(r'\\\w|\\\\', next_line))
                next_is_empty = not next_line.strip()
                
                if not next_has_latex or (next_is_empty and not any(re.search(r'\\\w|\\\\', lines[j]) for j in range(i+2, min(i+3, len(lines))))):
                    # 下一行不是LaTeX或是空行，结束数学块
                    output.append('$$')
                    in_math_block = False
            else:
                # 文件末尾，结束数学块
                output.append('$$')
                in_math_block = False
    else:
        # 不是LaTeX行
        if in_math_block:
            # 结束当前数学块
            output.append('$$')
            in_math_block = False
        
        output.append(line)
    
    i += 1

# 关闭任何未关闭的数学块
if in_math_block:
    output.append('$$')

# 保存修复后的内容
fixed_content = '\n'.join(output)

with open(markdown_file, 'w', encoding='utf-8') as f:
    f.write(fixed_content)

print("✓ 微分方程文章修复完成")
