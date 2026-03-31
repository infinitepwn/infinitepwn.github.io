#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

markdown_file = "/Users/infinite/Documents/blog/source/_posts/2024-12-20_微分方程.md"

with open(markdown_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 问题分析：
# 1. 公式直接嵌入在文本中，没有用$$包裹
# 2. 需要将 \frac, \int 等前面加上$$
# 3. 需要正确处理换行符

# 首先，让我们用更系统的方式重新格式化这个文件

# 将整个内容按照逻辑分解
# 使用正则表达式来识别和修复公式

# 策略：找到所有包含 \ 的行（LaTeX命令），为它们添加$$包裹

# 但这太复杂了。让我们直接从HTML重新提取

from html.parser import HTMLParser
import os

html_file = "/Users/infinite/Documents/blog-backup/post/20241220201200.html"

# 使用BeautifulSoup会更简单
try:
    from bs4 import BeautifulSoup
    
    with open(html_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
    
    # 找到文章内容
    article = soup.find('article')
    if article:
        # 获取所有内容
        content = article.get_text()
        print("✓ 成功从HTML提取内容")
        
        # 保存为临时文件以便检查
        with open('/tmp/diff_eq_content.txt', 'w', encoding='utf-8') as f:
            f.write(content)
    else:
        print("✗ 无法找到article标签")
        
except ImportError:
    print("BeautifulSoup not installed, installing...")
    os.system("pip install beautifulsoup4 -q")
    
    from bs4 import BeautifulSoup
    
    with open(html_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
    
    article = soup.find('article')
    if article:
        content = article.get_text()
        
        with open('/tmp/diff_eq_content.txt', 'w', encoding='utf-8') as f:
            f.write(content)

# 现在进行手动修复
# 问题：公式格式混乱，需要规范化

# 读取原始文件
with open(markdown_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 处理每一行
output_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    
    # 检查是否是公式行
    if '\\' in line and not line.strip().startswith('```'):
        # 这可能是一个公式行
        # 需要将其包裹在$$中
        
        # 检查是否已经有$$
        if '$$' not in line:
            # 需要添加$$
            # 但要小心不要破坏已有的结构
            
            # 如果行开始于 \ 或包含 \frac, \int 等
            if re.search(r'\\(frac|int|sum|prod|sqrt|left|right|begin|end|approx|equiv|neq|leq|geq|cdot|times|div|sin|cos|tan|log|ln|exp)', line):
                # 这是一个LaTeX公式行
                # 需要找到公式的起始和结束位置
                
                # 简单处理：如果整行都是公式，用$$包裹
                stripped = line.strip()
                if stripped and not stripped.startswith('#'):
                    # 这可能是公式
                    if '$$' not in stripped:
                        # 添加$$
                        if stripped.startswith('\\'):
                            line = '$$\n' + line
                        elif any(x in stripped for x in ['\\frac', '\\int', '\\sum']):
                            # 找到第一个\的位置
                            m = re.search(r'\\', stripped)
                            if m:
                                pos = m.start()
                                # 在\ 前面添加$$，在行尾添加$$
                                indent = len(line) - len(line.lstrip())
                                if pos == 0:
                                    # 从行首开始是公式
                                    line = ' ' * indent + '$$\n' + line + '$$\n'
                                else:
                                    # 公式在行中间
                                    before = line[:indent + pos]
                                    formula = line[indent + pos:].rstrip()
                                    line = before + '$$\n' + formula + '\n$$\n'
    
    output_lines.append(line)
    i += 1

# 实际上，这个方法太复杂了。让我重新思考。
# 问题是原始提取中，公式没有被正确格式化。
# 最简单的办法是：
# 1. 找出所有问题行
# 2. 手动修复

# 让我们直接修复这个文件

content = ''.join(lines)

# 这个文件的问题：
# 1. 每个"Example"和"Exercise"后面跟着的是公式，但没有$$包裹
# 2. 需要在所有包含\的段落前后加上$$

# 更精确的方法：使用更细粒度的正则替换

# 首先，让我们保持文件的基本结构，只修复公式部分

# 分割内容为各个section
sections = content.split('###')

fixed_sections = []
for i, section in enumerate(sections):
    if i == 0:
        # 保持第一部分（头部）不变
        fixed_sections.append(section)
    else:
        # 处理每个section
        # 逻辑：这个section中包含多个公式块
        # 需要找到并正确格式化它们
        
        # 简单处理：在section内，查找所有包含\ 的行
        lines = section.split('\n')
        fixed_lines = []
        
        in_formula = False
        for line in lines:
            if '\\' in line and not line.strip().startswith('```'):
                # 这是一个公式行
                if not in_formula:
                    fixed_lines.append('$$')
                    in_formula = True
                fixed_lines.append(line)
            elif in_formula and (line.strip() == '' or line.startswith('###') or not any(c in line for c in ['\\', '=', '+', '-'])):
                # 公式块结束
                fixed_lines.append('$$')
                fixed_lines.append(line)
                in_formula = False
            else:
                fixed_lines.append(line)
        
        if in_formula:
            fixed_lines.append('$$')
        
        fixed_sections.append('\n'.join(fixed_lines))

fixed_content = '###'.join(fixed_sections)

# 保存修复后的文件
with open(markdown_file, 'w', encoding='utf-8') as f:
    f.write(fixed_content)

print("✓ 文件修复完成")
