#!/usr/bin/env python3
"""
使用专业的 html-to-markdown 工具转换 HTML 文件
基于 Rust 编写，性能优秀，转换质量高
"""

import os
import sys
from pathlib import Path
from html_to_markdown import convert

def convert_html_to_markdown(html_file_path, output_md_file_path):
    """
    使用 html-to-markdown 库转换 HTML 到 Markdown
    """
    print(f"正在读取 HTML 文件: {html_file_path}")
    
    # 读取 HTML 文件
    with open(html_file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    print(f"HTML 文件大小: {len(html_content)} 字符")
    
    # 使用 html-to-markdown 进行转换
    print("正在使用 html-to-markdown 库进行转换...")
    result = convert(html_content, extract_metadata=True)
    
    # 获取转换后的 Markdown 内容
    markdown_content = result["content"]
    
    # 如果有元数据，也提取出来
    metadata = result.get("metadata", {})
    if metadata:
        print(f"提取到的元数据: {metadata}")
    
    print(f"转换后的 Markdown 大小: {len(markdown_content)} 字符")
    
    # 保存 Markdown 文件
    with open(output_md_file_path, 'w', encoding='utf-8') as f:
        f.write("# 计算机网络知识点总结\n\n")
        f.write("> 本文基于谢希仁《计算机网络（第八版）》第1-4章内容整理\n\n")
        
        # 添加一些元信息
        if metadata:
            f.write("## 📋 元信息\n\n")
            for key, value in metadata.items():
                if key != "content":  # 跳过内容本身
                    f.write(f"- **{key}**: {value}\n")
            f.write("\n")
        
        # 添加转换说明
        f.write("## 🔧 转换说明\n\n")
        f.write("本文使用专业的 `html-to-markdown` 工具转换，保留原格式和内容完整性。\n\n")
        f.write("---\n\n")
        
        # 写入转换后的内容
        f.write(markdown_content)
    
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