#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
改进的HTML转Markdown转换脚本 - 更完整地提取内容
"""

import os
import re
from datetime import datetime

def html_to_markdown_manual(html_file_path, output_dir):
    """
    手动处理HTML内容，更完整地转换为Markdown
    """
    # 读取HTML文件
    with open(html_file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # 提取主要内容区域
    # 寻找主要内容（可能在<div>或<main>标签中）
    content_match = re.search(r'<body[^>]*>(.*?)</body>', html_content, re.DOTALL)
    if content_match:
        body_content = content_match.group(1)
    else:
        body_content = html_content
    
    # 提取标题
    title_match = re.search(r'<title[^>]*>(.*?)</title>', html_content, re.DOTALL)
    title = title_match.group(1) if title_match else "计算机网络知识点总结（谢希仁第8版）"
    
    # 清理HTML标签，转换为Markdown格式
    markdown_content = convert_html_to_markdown(body_content)
    
    # 进一步优化格式
    markdown_content = optimize_markdown(markdown_content)
    
    # 获取当前日期
    today = datetime.now().strftime('%Y-%m-%d')
    
    # 创建Hexo文章头
    hexo_header = f"""---
title: {title}
date: {today} 11:00:00
tags:
  - 计算机网络
  - 学习笔记
  - 谢希仁
  - 网络基础
categories:
  - 计算机科学
  - 网络技术
---
    
"""
    
    # 组合完整内容
    full_content = hexo_header + markdown_content
    
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 生成输出文件名
    output_filename = f"{today}-计算机网络知识点完整总结.md"
    output_path = os.path.join(output_dir, output_filename)
    
    # 写入文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_content)
    
    print(f"✓ 改进版Markdown文件已生成: {output_path}")
    print(f"✓ 标题: {title}")
    print(f"✓ 日期: {today}")
    
    return output_path

def convert_html_to_markdown(html_text):
    """
    手动转换HTML为Markdown
    """
    # 移除脚本和样式
    html_text = re.sub(r'<script[^>]*>.*?</script>', '', html_text, flags=re.DOTALL)
    html_text = re.sub(r'<style[^>]*>.*?</style>', '', html_text, flags=re.DOTALL)
    
    # 转换标题
    for i in range(1, 7):
        html_text = re.sub(rf'<h{i}[^>]*>(.*?)</h{i}>', rf'\n\n{"#"*i} \g<1>\n\n', html_text, flags=re.DOTALL)
    
    # 转换段落
    html_text = re.sub(r'<p[^>]*>(.*?)</p>', r'\n\n\1\n\n', html_text, flags=re.DOTALL)
    
    # 转换列表
    html_text = re.sub(r'<li[^>]*>(.*?)</li>', r'* \1\n', html_text, flags=re.DOTALL)
    html_text = re.sub(r'<ul[^>]*>', '\n', html_text, flags=re.DOTALL)
    html_text = re.sub(r'</ul>', '\n', html_text, flags=re.DOTALL)
    html_text = re.sub(r'<ol[^>]*>', '\n', html_text, flags=re.DOTALL)
    html_text = re.sub(r'</ol>', '\n', html_text, flags=re.DOTALL)
    
    # 转换粗体
    html_text = re.sub(r'<strong[^>]*>(.*?)</strong>', r'**\1**', html_text, flags=re.DOTALL)
    html_text = re.sub(r'<b[^>]*>(.*?)</b>', r'**\1**', html_text, flags=re.DOTALL)
    
    # 转换斜体
    html_text = re.sub(r'<em[^>]*>(.*?)</em>', r'*\1*', html_text, flags=re.DOTALL)
    html_text = re.sub(r'<i[^>]*>(.*?)</i>', r'*\1*', html_text, flags=re.DOTALL)
    
    # 转换链接
    html_text = re.sub(r'<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>', r'[\2](\1)', html_text, flags=re.DOTALL)
    
    # 转换代码
    html_text = re.sub(r'<code[^>]*>(.*?)</code>', r'`\1`', html_text, flags=re.DOTALL)
    
    # 转换代码块
    html_text = re.sub(r'<pre[^>]*>(.*?)</pre>', r'\n```\n\1\n```\n', html_text, flags=re.DOTALL)
    
    # 转换表格（简化处理）
    html_text = re.sub(r'<table[^>]*>', '\n\n| ', html_text, flags=re.DOTALL)
    html_text = re.sub(r'</table>', ' |\n\n', html_text, flags=re.DOTALL)
    html_text = re.sub(r'<tr[^>]*>', '| ', html_text)
    html_text = re.sub(r'</tr>', ' |\n', html_text)
    html_text = re.sub(r'<td[^>]*>(.*?)</td>', r'\1 | ', html_text, flags=re.DOTALL)
    html_text = re.sub(r'<th[^>]*>(.*?)</th>', r'**\1** | ', html_text, flags=re.DOTALL)
    
    # 移除其他HTML标签
    html_text = re.sub(r'<[^>]+>', '', html_text)
    
    # 清理HTML实体
    html_text = html_text.replace('&nbsp;', ' ')
    html_text = html_text.replace('&lt;', '<')
    html_text = html_text.replace('&gt;', '>')
    html_text = html_text.replace('&amp;', '&')
    html_text = html_text.replace('&quot;', '"')
    html_text = html_text.replace('&#39;', "'")
    
    return html_text

def optimize_markdown(markdown_text):
    """
    优化Markdown格式
    """
    # 移除过多的空行
    markdown_text = re.sub(r'\n\s*\n\s*\n+', '\n\n', markdown_text)
    
    # 修复标题前后的空行
    for i in range(1, 7):
        markdown_text = re.sub(rf'([^\n])\n({{i}} )', rf'\1\n\n\2 ', markdown_text)
        markdown_text = re.sub(rf'({{i}} .*?)\n([^\n])', rf'\1\n\n\2', markdown_text)
    
    # 添加emoji和格式美化
    # 给重要的标题添加emoji
    emoji_patterns = [
        (r'第一章.*?概论', '📡'),
        (r'第二章.*?物理层', '🔌'),
        (r'第三章.*?数据链路层', '🔗'),
        (r'第四章.*?网络层', '🌐'),
        (r'定义.*?核心定义', '📖'),
        (r'生活例子.*?', '🌰'),
        (r'个人理解.*?', '💡'),
        (r'表格.*?', '📊'),
        (r'注意.*?', '⚠️'),
        (r'性能指标.*?', '⚡'),
        (r'时延.*?', '⏱️'),
        (r'核心重点.*?', '⭐'),
    ]
    
    for pattern, emoji in emoji_patterns:
        markdown_text = re.sub(pattern, f'{emoji} \\g<0>', markdown_text)
    
    return markdown_text

def main():
    # 输入文件路径
    html_file = "/Users/infinite/WorkBuddy/20260330101903/计算机网络知识点总结.html"
    
    # 输出目录
    output_dir = "/Users/infinite/Documents/blog/source/_posts"
    
    # 检查文件是否存在
    if not os.path.exists(html_file):
        print(f"❌ HTML文件不存在: {html_file}")
        return
    
    print(f"开始转换HTML文件: {html_file}")
    print(f"输出目录: {output_dir}")
    
    try:
        # 备份原来的文件
        original_file = os.path.join(output_dir, "2026-04-01-计算机网络知识点总结.md")
        if os.path.exists(original_file):
            backup_file = original_file + ".backup"
            os.rename(original_file, backup_file)
            print(f"✓ 已备份原文件到: {backup_file}")
        
        output_file = html_to_markdown_manual(html_file, output_dir)
        print(f"\n转换完成！文件已保存到: {output_file}")
        print(f"文件大小: {os.path.getsize(output_file)} 字节")
        
        # 读取文件行数
        with open(output_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            print(f"行数: {len(lines)} 行")
        
        print("\n使用以下命令预览文章:")
        print("cd /Users/infinite/Documents/blog")
        print("hexo server -p 8888")
        
    except Exception as e:
        print(f"❌ 转换过程中发生错误: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()