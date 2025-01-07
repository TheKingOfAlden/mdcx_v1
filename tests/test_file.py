import os
import sys
import tempfile
import re
import traceback
from unittest import TestCase, main

from models.signals import signal


def parse_directory_tree_test(tree_file_path: str) -> list:
    # 从配置中获取媒体类型
    media_extensions = [".mp4", ".mkv", ".avi", ".rmvb", ".wmv", ".mov", ".flv", ".ts", ".webm", ".iso", ".mpg"]
    movie_list = []
    current_path = []
    prefix_pattern = re.compile(r'^(\| )+')

    try:
        # 读取目录树文件
        with open(tree_file_path, 'r', encoding='utf-16 LE') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                # 跳过根目录行
                if '|' not in line:
                    continue

                # 提取当前行的文件夹/文件名并清理
                parts = line.split('|-')
                if len(parts) < 2:
                    continue
                name = parts[-1].strip()
                if name.startswith('-'):
                    name = name[1:].strip()

                # 计算深度（通过匹配前导的 "| " 数量）
                match = prefix_pattern.match(line)
                if match:
                    depth = len(match.group(0)) // 2  # 每个“| ”占两个字符
                else:
                    depth = 0

                # 根据深度更新当前路径
                while len(current_path) > depth:
                    current_path.pop()
                if len(current_path) < depth:
                    current_path.append(name)
                else:
                    current_path[depth-1] = name

                # 检查是否为视频文件
                if any(name.lower().endswith(ext) for ext in media_extensions):
                    # 构建完整文件路径，添加前缀
                    full_path = os.path.join(*current_path)
                    print(full_path)
                    movie_list.append(full_path)

    except Exception as e:
        signal.show_log_text(f'Error reading directory tree file: {str(e)}')
        signal.show_traceback_log(traceback.format_exc())

    return movie_list


class TestParseDirectoryTree(TestCase):

    def test_parse_directory_tree(self):
        print("\n=== 开始测试 ===")
        # 测试带/H/前缀的情况
        movie_list = parse_directory_tree_test("/Users/lianghangfei/Desktop/根目录20241230011514_目录树.txt")

        # 打印第一个文件的路径
        if movie_list:
            path = movie_list[0]
            print("\n=== 测试结果 ===")
            print("原始路径:")
            print(path)
            print("\n替换后路径:")
            # 拼接前缀/H/
            full_path = os.path.join("/H/115/", path)
            print(full_path)
            print(f"\n共找到 {len(movie_list)} 个视频文件")
        else:
            print("\n未找到任何视频文件")
        print("\n=== 测试结束 ===")


if __name__ == '__main__':
    main()
