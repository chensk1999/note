import re
from pathlib import Path

def find_unreferenced_images(base_dir:str):
    """
    扫描 Markdown 文件中引用的图片，找出未被引用的文件、缺失的图片

    Parameters:
        base_dir: str 笔记的根目录，如 notes/
        image_subdir: 图片所在子目录，如 images/

    返回:
        unreferenced, missing
        未被引用的图片路径列表、缺失的图片路径
    """
    base = Path(base_dir)

    # 收集所有图片文件（常见图片扩展名）
    img_ext = [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".svg", ".webp"]
    image_files = {
        p.resolve() for p in base.rglob("*") if p.suffix.lower() in img_ext
    }

    # 正则匹配 Markdown 和 HTML 图片引用
    pattern_md = re.compile(r'!\[[^\]]*\]\(([^)]+)\)')
    referenced = set()

    # 遍历所有 Markdown 文件
    for md_file in base.rglob("*.md"):
        text = md_file.read_text(encoding="utf-8", errors="ignore")
        matches = pattern_md.findall(text)

        for m in matches:
            # 统一路径形式
            img_relpath = m.strip().split("?")[0].split("#")[0]
            if not img_relpath:
                continue
            # 忽略 base64 图片
            if img_relpath.startswith("data:image"):
                continue
            img_abspath = md_file.parent / img_relpath
            # 记录引用路径
            referenced.add(Path(img_abspath).resolve())

    # 找出未被引用的图片、缺失的图片
    unreferenced = sorted(image_files - referenced)
    missing = sorted(referenced - image_files)
    return unreferenced, missing


if __name__ == "__main__":
    unused, missing = find_unreferenced_images("..")

    if unused:
        print("未被引用的图片：")
        for img in unused:
            print(" -", img)
    if missing:
        print("缺失的图片：")
        for img in missing:
            print(" -", img)
    if not unused and not missing:
        print("所有图片均已被引用")
