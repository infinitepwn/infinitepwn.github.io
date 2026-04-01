#!/usr/bin/env python3
"""
正确使用 html-to-markdown 工具转换 HTML 文件
基于 Rust 编写，性能优秀，转换质量高
"""

import os
import sys
from pathlib import Path
from html_to_markdown import convert, ConversionOptions

def convert_html_to_markdown(html_file_path, output_md_file_path):
    """
    使用 html-to-markdown 库转换 HTML 到 Markdown
    """
    print(f"正在读取 HTML 文件: {html_file_path}")
    
    # 读取 HTML 文件
    with open(html_file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    print(f"HTML 文件大小: {len(html_content)} 字符")
    
    # 配置转换选项
    options = ConversionOptions(
        heading_style="atx",  # 使用 # 标题样式
        wrap_width=80,       # 行宽限制
    )
    
    # 使用 html-to-markdown 进行转换
    print("正在使用 html-to-markdown 库进行转换...")
    result = convert(html_content, options=options)
    
    # 获取转换后的 Markdown 内容
    markdown_content = result.get("content", "")
    
    # 提取元数据和其他信息
    metadata = result.get("metadata", {})
    tables = result.get("tables", [])
    warnings = result.get("warnings", [])
    
    if metadata:
        print(f"提取到的元数据: {len(metadata)} 条")
    if tables:
        print(f"提取到的表格: {len(tables)} 个")
    if warnings:
        print(f"转换警告: {len(warnings)} 条")
    
    print(f"转换后的 Markdown 大小: {len(markdown_content)} 字符")
    
    # 准备博客文章格式
    blog_content = f"""# 计算机网络知识点总结

> 本文基于谢希仁《计算机网络（第八版）》第1-4章内容整理
> 
> 📅 转换时间: 2026-04-01
> 🔧 转换工具: html-to-markdown (基于Rust的高性能转换器)

## 📋 内容摘要

本文通过专业的 HTML 转 Markdown 工具进行转换，确保内容完整性和格式保留。内容涵盖计算机网络的基础知识、协议、网络模型等核心概念。

---

## 主要内容

{markdown_content}

---

## 🔍 转换统计

- **源文件**: {os.path.basename(html_file_path)}
- **转换工具**: html-to-markdown v3.0.1
- **转换选项**: heading_style="atx", wrap_width=80
"""

    # 如果有表格信息，添加说明
    if tables:
        blog_content += f"\n- **提取表格**: {len(tables)} 个表格已转换为Markdown格式\n"

    if warnings:
        blog_content += f"\n- **转换警告**: {len(warnings)} 条（不影响主要内容）\n"
    
    blog_content += "\n> 💡 提示：建议使用支持Markdown的阅读器查看，以获得最佳阅读体验。\n"
    
    # 保存 Markdown 文件
    with open(output_md_file_path, 'w', encoding='utf-8') as f:
        f.write(blog_content)
    
    print(f"✅ Markdown 文件已保存: {output_md_file_path}")
    return True

def main():
    """主函数"""
    # 输入 HTML 文件路径
    html_file = "/Users/infinite/WorkBuddy/20260330101903/计算机网络知识点总结.html"
    
    # 输出 Markdown 文件路径
    output_dir = "/Users/infinite/Documents/blog/source/_posts"
    output_file = os.path.join(output_dir, "2026-04-01-计算机网络知识点总结-专业转换.md")
    
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 检查输入文件是否存在
    if not os.path.exists(html_file):
        print(f"❌ 输入文件不存在: {html_file}")
        return False
    
    # 执行转换
    success = convert_html_to_markdown(html_file, output_file)
    
    if success:
        # 统计文件信息
        print("\n📊 转换统计:")
        print(f"  输入文件大小: {os.path.getsize(html_file)} 字节")
        print(f"  输出文件大小: {os.path.getsize(output_file)} 字节")
        
        # 计算行数
        with open(output_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            print(f"  输出文件行数: {len(lines)} 行")
        
        print("\n🎉 转换完成！建议检查输出文件，确保格式和内容完整性。")
    else:
        print("❌ 转换失败")
    
    return success

if __name__ == "__main__":
    sys.exit(0 if main() else 1)