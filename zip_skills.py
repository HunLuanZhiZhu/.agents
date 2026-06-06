#!/usr/bin/env python3
"""
将 skills/ 目录下的每个子文件夹打包成独立的压缩包。
每个子文件夹生成一个同名的 .zip 文件，存放在 skills/ 目录下。
"""

import os
import zipfile
from pathlib import Path


def zip_directory(source_dir: Path, output_path: Path):
    """将 source_dir 打包成 zip 文件，输出到 output_path。"""
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                file_path = Path(root) / file
                # 使用相对路径，避免包含绝对路径前缀
                arcname = file_path.relative_to(source_dir.parent)
                zf.write(file_path, arcname)


def main():
    skills_dir = Path(__file__).parent / 'skills'
    
    if not skills_dir.exists():
        print(f"Error: Directory not found: {skills_dir}")
        return
    
    # 遍历 skills/ 下的所有子文件夹
    for item in skills_dir.iterdir():
        if item.is_dir():
            zip_path = skills_dir / f"{item.name}.zip"
            print(f"Packing: {item.name} -> {zip_path.name}")
            try:
                zip_directory(item, zip_path)
                print(f"  Done: {zip_path}")
            except Exception as e:
                print(f"  Failed: {e}")

    print("\nAll done!")


if __name__ == '__main__':
    main()
