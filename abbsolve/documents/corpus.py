"""
A corpus generator for reading documents from a directory.
"""

import os
from typing import Generator


def txt_generator(corpus_dir: str) -> Generator[str, None, None]:
    """
    A file handler that reads and yields the content of all .txt files in a directory and its subdirectories.

    Args:
        corpus_dir: a directory containing .txt files, possibly nested in multiple subdirectories of arbitrary depth

    Yields:
        content of each .txt file as a string

    """
    for root, _, files in os.walk(corpus_dir):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        yield f.read()
                except Exception as e:
                    print(f"Error reading file {file_path}: {e}")

