#!/usr/bin/env python3
"""
将 skills/ 目录下的每个子文件夹异步打包成独立的压缩包。
每个子文件夹生成一个同名的 .zip 文件，存放在 skills/ 目录下。
"""

import asyncio
import os
import zipfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


def zip_directory_sync(source_dir: Path, output_path: Path):
    """同步函数：将 source_dir 打包成 zip 文件。"""
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                file_path = Path(root) / file
                # 使用相对路径，避免包含绝对路径前缀
                arcname = file_path.relative_to(source_dir.parent)
                zf.write(file_path, arcname)


async def zip_directory(source_dir: Path, output_path: Path, executor: ThreadPoolExecutor):
    """异步包装：在线程池中执行 zip 打包。"""
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(executor, zip_directory_sync, source_dir, output_path)


async def main():
    skills_dir = Path(__file__).parent / 'skills'

    if not skills_dir.exists():
        print(f"Error: Directory not found: {skills_dir}")
        return

    # 收集所有需要打包的子文件夹
    tasks = []
    dirs_to_pack = [item for item in skills_dir.iterdir() if item.is_dir()]

    # 使用线程池并发执行打包（IO 密集型，线程池比多进程更合适）
    with ThreadPoolExecutor() as executor:
        for item in dirs_to_pack:
            zip_path = skills_dir / f"{item.name}.zip"
            print(f"Queueing: {item.name} -> {zip_path.name}")
            tasks.append(zip_directory(item, zip_path, executor))

        # 并发执行所有打包任务
        results = await asyncio.gather(*tasks, return_exceptions=True)

    # 输出结果
    for item, result in zip(dirs_to_pack, results):
        zip_path = skills_dir / f"{item.name}.zip"
        if isinstance(result, Exception):
            print(f"  Failed: {item.name} -> {result}")
        else:
            print(f"  Done: {item.name} -> {zip_path}")

    print(f"\nAll done! Packed {len(dirs_to_pack)} directories.")


if __name__ == '__main__':
    asyncio.run(main())
