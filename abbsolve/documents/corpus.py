"""
A corpus generator for reading documents from a directory.
"""

import os
from typing import Generator

from pypdf import PdfReader


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


def pdf_generator(corpus_dir: str) -> Generator[str, None, None]:
    """
    A file handler that reads and yields the content of all .pdf files in a directory and its subdirectories. This
    function will generally only work with "digitally native" PDFs with embedded text, and not scanned documents.

    Args:
        corpus_dir: a directory containing .pdf files, possibly nested in multiple subdirectories of arbitrary depth

    Yields:
        content of each .pdf file as a string

    """
    for root, _, files in os.walk(corpus_dir):
        for file in files:
            if file.endswith(".pdf"):
                file_path = os.path.join(root, file)
                try:
                    reader = PdfReader(file_path)
                    text = ""
                    for page in reader.pages:
                        text += page.extract_text() or ""
                    yield text
                except Exception as e:
                    print(f"Error reading PDF file {file_path}: {e}")
