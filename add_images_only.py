#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
只添加图片引用到现有的Markdown文章中
"""

import re
from pathlib import Path

# 图片映射关系：从HTML中的图片路径 -> CDN URL + 文章标识
images_map = {
    "array": {
        "filename": "QQ_1731931863751.png",
        "src": "/2024/11/18/array/QQ_1731931863751.png"
    },
    "pointer": {
        "filename": "image-20241128142813450.png",
        "src": "/2024/11/28/pointer/image-20241128142813450.png"
    }
}

CDN_BASE = "https://raw.githubusercontent.com/infinitepwn/blogimage/main"

def add_images_to_article(md_path, image_info):
    """为文章添加图片引用"""
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 如果已经有这个图片引用了，就跳过
    if image_info["filename"] in content:
        print(f"  ⊘ {md_path.name}: 已包含该图片")
        return False
    
    # 构建CDN URL
    cdn_url = f"{CDN_BASE}/{image_info['filename']}"
    image_md = f"![{image_info['filename']}]({cdn_url})\n\n"
    
    # 在文章正文的开始部分（Front Matter之后）添加图片
    # 找到第二个 --- 之后的位置
    parts = content.split('---', 2)
    if len(parts) == 3:
        # parts[0] 是空的, parts[1] 是 Front Matter, parts[2] 是正文
        new_content = '---' + parts[1] + '---\n\n' + image_md + parts[2]
    else:
        # 如果没有Front Matter，就在最开始添加
        new_content = image_md + content
    
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"  ✓ {md_path.name}: 已添加图片")
    return True

def main():
    posts_dir = Path("/Users/infinite/Documents/blog/source/_posts")
    
    # 为array文章添加图片
    array_file = list(posts_dir.glob("*array.md"))
    if array_file:
        print(f"\n📄 处理 array 文章")
        add_images_to_article(array_file[0], images_map["array"])
    
    # 为pointer文章添加图片
    pointer_file = list(posts_dir.glob("*pointer.md"))
    if pointer_file:
        print(f"\n📄 处理 pointer 文章")
        add_images_to_article(pointer_file[0], images_map["pointer"])
    
    print("\n✅ 完成！")

if __name__ == '__main__':
    main()
