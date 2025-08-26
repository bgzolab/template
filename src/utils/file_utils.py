#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author : bGZo
@Date : 2025-07-27
@Links : https://github.com/bGZo
"""
import re
import os

def output_content_to_file_path(file_dir: str, file_name: str, content: str, file_type: str = "md") -> str:
    output_path = output_file_path(file_dir, file_name, file_type)
    ensure_output_directory_exists(file_dir)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    return output_path


def output_file_path(file_dir: str, file_name: str, file_type: str = "md") -> str:
    return os.path.join(file_dir, f"~{file_name}.{file_type}")

def ensure_output_directory_exists(output_dir: str):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Output directory '{output_dir}' created.")


def get_clean_filename(filename: str) -> str:
    try:
        filename = re.sub(r'[@…：.？，！\|｜【】\[\]:!“”《》_、「」#——<>:"/\\|\-。（）&•]', ' ', filename)
    except AttributeError:
        pass

    filename = re.sub(r'[ ]+', ' ', filename)
    filename = filename.strip()
    filename = re.sub(r' ', '-', filename)
    return filename
