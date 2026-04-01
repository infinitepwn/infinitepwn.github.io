#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将计算机网络知识点总结.html转换为Hexo博客Markdown格式
"""

import os
import re
from bs4 import BeautifulSoup
import markdownify
from datetime import datetime

def html_to_markdown(html_file_path, output_dir):
    """
    将HTML文件转换为Markdown格式
    """
    # 读取HTML文件
    with open(html_file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # 使用BeautifulSoup解析
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 提取标题
    title = "计算机网络知识点总结（谢希仁第8版）"
    
    # 提取主要内容
    content_div = soup.find('div', {'id': 'content'})
    if not content_div:
        content_div = soup.find('div', {'class': 'content'})
    if not content_div:
        content_div = soup.find('body')
    
    # 获取文本内容
    html_for_conversion = str(content_div) if content_div else html_content
    
    # 使用markdownify转换HTML为Markdown
    markdown_content = markdownify.markdownify(
        html_for_conversion,
        heading_style='ATX',  # 使用#格式的标题
        bullets='*'  # 使用星号作为列表符号
    )
    
    # 清理Markdown内容
    markdown_content = clean_markdown(markdown_content)
    
    # 获取当前日期
    today = datetime.now().strftime('%Y-%m-%d')
    
    # 创建Hexo文章头
    hexo_header = f"""---
title: {title}
date: {today} 10:00:00
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
    output_filename = f"{today}-计算机网络知识点总结.md"
    output_path = os.path.join(output_dir, output_filename)
    
    # 写入文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_content)
    
    print(f"✓ Markdown文件已生成: {output_path}")
    print(f"✓ 标题: {title}")
    print(f"✓ 日期: {today}")
    
    return output_path

def clean_markdown(markdown_text):
    """
    清理和优化Markdown文本
    """
    # 移除过多的空行
    markdown_text = re.sub(r'\n\s*\n\s*\n+', '\n\n', markdown_text)
    
    # 修复代码块格式
    markdown_text = re.sub(r'```\s*\n', '```\n', markdown_text)
    markdown_text = re.sub(r'\n```', '\n```', markdown_text)
    
    # 修复标题格式（确保标题前后有空行）
    for i in range(1, 7):
        markdown_text = re.sub(rf'([^\n])\n({{i}}) ', rf'\1\n\n\2 ', markdown_text)
    
    # 修复表格格式
    markdown_text = re.sub(r'\|\s*\n', '|\n', markdown_text)
    
    # 移除HTML注释
    markdown_text = re.sub(r'<!--.*?-->', '', markdown_text, flags=re.DOTALL)
    
    return markdown_text

def main():
    # 输入文件路径
    html_file = "/Users/infinite/WorkBuddy/20260330101903/计算机网络知识点总结.html"
    
    # 输出目录（博客的_posts目录）
    output_dir = "/Users/infinite/Documents/blog/source/_posts"
    
    # 检查文件是否存在
    if not os.path.exists(html_file):
        print(f"❌ HTML文件不存在: {html_file}")
        return
    
    print(f"开始转换HTML文件: {html_file}")
    print(f"输出目录: {output_dir}")
    
    try:
        output_file = html_to_markdown(html_file, output_dir)
        print(f"\n转换完成！文件已保存到: {output_file}")
        print("\n使用以下命令预览文章:")
        print("cd /Users/infinite/Documents/blog")
        print("hexo server -p 9999")
        print("\n部署到博客:")
        print("./deploy.sh \"添加计算机网络知识点总结\"")
    except Exception as e:
        print(f"❌ 转换过程中发生错误: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()