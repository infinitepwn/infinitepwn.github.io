#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将计算机网络笔记HTML转换为Hexo博客Markdown格式
"""

import re
from bs4 import BeautifulSoup

def html_to_markdown(html_content):
    """
    将HTML内容转换为Markdown格式
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 移除所有样式标签
    for style_tag in soup.find_all('style'):
        style_tag.decompose()
    
    # 获取标题
    title_tag = soup.find('title')
    title = title_tag.text if title_tag else "计算机网络知识点总结"
    
    # 获取主要内容
    content_div = soup.find('div', class_='container')
    
    if not content_div:
        # 如果没有找到容器，使用整个body
        content_div = soup.body
    
    # 转换函数
    def convert_element(element, level=0):
        if element.name is None:
            return str(element) if element.strip() else ""
        
        # 处理不同标签
        if element.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            level = int(element.name[1])
            text = element.get_text().strip()
            return '\n' + '#' * level + ' ' + text + '\n\n'
        
        elif element.name == 'p':
            text = element.get_text().strip()
            if text:
                return text + '\n\n'
            return ''
        
        elif element.name == 'div':
            # 检查是否是特殊样式的div
            classes = element.get('class', [])
            if 'chapter' in classes:
                # 章节标题
                header = element.find(class_='chapter-header')
                if header:
                    h2 = header.find('h2')
                    if h2:
                        return '\n## ' + h2.get_text().strip() + '\n\n'
            
            elif 'section' in classes:
                # 小节标题
                title_div = element.find(class_='section-title')
                if title_div:
                    return '\n### ' + title_div.get_text().strip() + '\n\n'
            
            elif 'kcard' in classes:
                # 知识点卡片
                content_text = ''
                # 获取标题
                title_div = element.find(class_='kcard-title')
                if title_div:
                    # 移除表情符号和标签
                    title_text = title_div.get_text().strip()
                    title_text = re.sub(r'<span[^>]*>.*?</span>', '', str(title_div), flags=re.DOTALL)
                    title_text = re.sub(r'<[^>]+>', '', title_text)  # 移除HTML标签
                    title_text = title_text.strip()
                    content_text += '**' + title_text + '**\n\n'
                
                # 获取内容
                for p in element.find_all('p'):
                    p_text = p.get_text().strip()
                    if p_text:
                        content_text += p_text + '\n\n'
                
                # 获取表格
                tables = element.find_all('table')
                for table in tables:
                    content_text += convert_table(table) + '\n\n'
                
                # 获取示例和见解
                for example in element.find_all(class_=['example', 'insight']):
                    example_text = example.get_text().strip()
                    if example_text:
                        if 'example' in example.get('class', []):
                            content_text += '> **🌰 例子：** ' + example_text + '\n\n'
                        elif 'insight' in example.get('class', []):
                            content_text += '> **💡 理解：** ' + example_text + '\n\n'
                
                # 获取提示框
                for callout in element.find_all(class_='callout'):
                    callout_text = callout.get_text().strip()
                    if callout_text:
                        content_text += '> ' + callout_text + '\n\n'
                
                return content_text
            
            # 递归处理子元素
            content = ''
            for child in element.children:
                content += convert_element(child, level)
            return content
        
        elif element.name == 'table':
            return convert_table(element) + '\n\n'
        
        elif element.name == 'ul' or element.name == 'ol':
            content = ''
            for li in element.find_all('li', recursive=False):
                li_text = li.get_text().strip()
                if li_text:
                    prefix = '- ' if element.name == 'ul' else '1. '
                    content += prefix + li_text + '\n'
            return content + '\n'
        
        elif element.name == 'li':
            # 在ul/ol中处理，这里不单独处理
            return ''
        
        elif element.name in ['strong', 'b']:
            text = element.get_text().strip()
            if text:
                return '**' + text + '**'
            return ''
        
        elif element.name == 'code':
            text = element.get_text().strip()
            if text:
                return '`' + text + '`'
            return ''
        
        elif element.name == 'a':
            text = element.get_text().strip()
            href = element.get('href', '')
            if text and href:
                return f'[{text}]({href})'
            return text or ''
        
        else:
            # 递归处理其他元素
            content = ''
            for child in element.children:
                content += convert_element(child, level)
            return content
    
    def convert_table(table):
        """转换表格为Markdown格式"""
        rows = table.find_all('tr')
        if not rows:
            return ''
        
        markdown_table = []
        
        # 处理表头
        headers = []
        header_row = rows[0]
        for th in header_row.find_all(['th', 'td']):
            headers.append(th.get_text().strip())
        
        markdown_table.append('| ' + ' | '.join(headers) + ' |')
        markdown_table.append('|' + '---|' * len(headers))
        
        # 处理数据行
        for row in rows[1:]:
            cells = []
            for td in row.find_all(['td', 'th']):
                cells.append(td.get_text().strip())
            markdown_table.append('| ' + ' | '.join(cells) + ' |')
        
        return '\n'.join(markdown_table)
    
    # 转换主要内容
    markdown_content = convert_element(content_div)
    
    # 清理多余的空行
    markdown_content = re.sub(r'\n{3,}', '\n\n', markdown_content)
    
    # 添加标题和引言
    final_content = f"""# 📡 计算机网络知识点全面总结

> 基于谢希仁《计算机网络》第八版（上册）整理，涵盖第1-4章：概论 · 物理层 · 数据链路层 · 网络层

{markdown_content}

---

**总结时间**：{title}
**学习心得**：计算机网络是连接数字世界的基础，理解其原理对编程、网络安全、系统架构都有重要意义。

> 💡 **学习建议**：多结合实际场景思考，比如访问网页时经历了哪些协议层次，数据包是怎么路由的，为什么有时网络会卡顿等。
"""
    
    return final_content

def main():
    # 读取HTML文件
    with open('/Users/infinite/WorkBuddy/20260330101903/计算机网络知识点总结.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # 转换为Markdown
    markdown_content = html_to_markdown(html_content)
    
    # 读取现有的Markdown文件头
    with open('/Users/infinite/Documents/blog/source/_posts/计算机网络笔记.md', 'r', encoding='utf-8') as f:
        existing_content = f.read()
    
    # 合并内容
    final_content = existing_content + '\n\n' + markdown_content
    
    # 写回文件
    with open('/Users/infinite/Documents/blog/source/_posts/计算机网络笔记.md', 'w', encoding='utf-8') as f:
        f.write(final_content)
    
    print("✅ 转换完成！Markdown文件已更新。")

if __name__ == '__main__':
    main()