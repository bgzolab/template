#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author : bGZo
@Date : 2025-07-27
@Links : https://github.com/bGZo
"""


def output_content_to_file_path(file_name: str, content: str, file_type: str = "md") -> str:
    """
    Writes content to a file and returns the file path.

    Args:
        file_name (str): The name of the file.
        content (str): The content to write to the file.
        file_type (str): The type of the file (default is "md").

    Returns:
        str: The full path to the output file.
    """
    import os

    output_path = output_file_path(file_name, file_type)
    # ensure_output_directory_exists(output_path)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    return output_path


def output_file_path(file_name: str, file_type: str = "md") -> str:
    """
    Generates a file path for output files based on the provided file name and type.

    Args:
        file_name (str): The name of the file.
        file_type (str): The type of the file (default is "md").

    Returns:
        str: The full path to the output file.
    """
    import os
    return os.path.join("output", f"~{file_name}.{file_type}")

def ensure_output_directory_exists(output_dir: str):
    """
    Ensures that the output directory exists. If it does not exist, it creates the directory.
    """
    import os

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Output directory '{output_dir}' created.")
    else:
        print(f"Output directory '{output_dir}' already exists.")
