# -*- coding: utf-8 -*-
"""
把 D:\\ai娜娜\\弦高\\新建文件夹 里的 .livp（iPhone Live Photo）转成普通 JPG 图片
输出到同一文件夹，文件名不变，只改后缀为 .jpg

使用方法：
  1. 安装 Python（https://www.python.org 下载，安装时勾选 "Add to PATH"）
  2. 打开命令行（Win+R 输入 cmd 回车），执行：
       pip install pillow pillow-heif
  3. 把这个脚本放到桌面（或任意位置），双击运行，或命令行执行：
       python convert_livp.py
"""

import io
import sys
import zipfile
from pathlib import Path

# 依赖包安装在 D 盘（不占用 C 盘空间）
sys.path.insert(0, r"D:\pylibs")

try:
    from PIL import Image
    import pillow_heif
except ImportError:
    print("缺少依赖，请先在命令行运行:  py -m pip install --target=D:\\pylibs pillow pillow-heif")
    input("按回车退出...")
    raise SystemExit(1)

pillow_heif.register_heif_opener()

FOLDER = Path(r"D:\ai娜娜\弦高\新建文件夹")

IMG_EXTS = (".heic", ".heif", ".jpg", ".jpeg", ".png")


def convert_one(livp: Path):
    """从 .livp / .zip 里取出照片，转成 .jpg 存到同目录"""
    with zipfile.ZipFile(livp) as z:
        # 找出压缩包里的照片文件（livp 里通常是一个 heic + 一个 mov）
        names = [n for n in z.namelist() if n.lower().endswith(IMG_EXTS)]
        if not names:
            print(f"[跳过] {livp.name}  （里面没有找到照片）")
            return
        data = z.read(names[0])

    img = Image.open(io.BytesIO(data)).convert("RGB")
    out = livp.with_suffix(".jpg")
    img.save(out, "JPEG", quality=95)
    print(f"[完成] {livp.name}  ->  {out.name}")


def main():
    if not FOLDER.exists():
        print(f"找不到文件夹: {FOLDER}")
        input("按回车退出...")
        return

    files = sorted(
        p for p in FOLDER.iterdir()
        if p.suffix.lower() in (".livp", ".zip")
    )
    if not files:
        print("文件夹里没有 .livp 或 .zip 文件")
        input("按回车退出...")
        return

    print(f"共找到 {len(files)} 个文件，开始转换...\n")
    ok = fail = 0
    for f in files:
        try:
            convert_one(f)
            ok += 1
        except Exception as e:
            fail += 1
            print(f"[失败] {f.name}  原因: {e}")

    print(f"\n全部结束：成功 {ok} 个，失败 {fail} 个")
    print(f"JPG 已保存到: {FOLDER}")
    input("按回车退出...")


if __name__ == "__main__":
    main()
