"""
A class for finding initialism inversion candidates using regex-based search across text files.
"""

import os
from typing import List, Set

from abbsolve.documents.corpus import txt_generator
from abbsolve.utils.regex import get_initialism_candidates


class RegexInitialismInverter:
    """
    A class that finds inversion candidates for an initialism by searching all txt files
    in a specified directory using regex-based pattern matching.
    """

    def __init__(self, initialism: str, directory: str):
        """
        Initialize the RegexInitialismInverter.

        Args:
            initialism: The initialism to find inversions for
            directory: The directory path containing txt files to search

        Raises:
            ValueError: If the directory doesn't exist or initialism is empty
        """
        if not initialism or not initialism.strip():
            raise ValueError("Initialism cannot be empty")

        if not os.path.exists(directory):
            raise ValueError(f"Directory does not exist: {directory}")

        if not os.path.isdir(directory):
            raise ValueError(f"Path is not a directory: {directory}")

        self.initialism = initialism.strip()
        self.directory = directory

    def find_candidates(self, stopwords: List[str] | None = None) -> Set[str]:
        """
        Find all inversion candidates for the initialism by searching txt files in the directory.

        Args:
            stopwords: Optional list of stopwords to allow between n-gram terms.
                      If None, uses default English stopwords.

        Returns:
            A set of candidate expansions found across all txt files
        """
        all_candidates = set()

        # iterate over the generator and accumulate the candidates
        for file_content in txt_generator(self.directory):
            candidates = get_initialism_candidates(
                self.initialism, file_content, stopwords
            )
            all_candidates.update(candidates)

        return all_candidates

    def find_candidates_with_sources(
            self, stopwords: List[str] | None = None
    ) -> dict[str, List[str]]:
        """
        Find inversion candidates along with the source files where they were found.

        Similar to find_candidates, but slightly slower and more memory consumptive,
        as it keeps track of where the candidates were found.

        Args:
            stopwords: Optional list of stopwords to allow between n-gram terms.
                      If None, uses default English stopwords.

        Returns:
            A dictionary mapping candidate expansions to lists of source file paths
        """
        candidates_with_sources = {}

        # walk the directory to get files containing candidates, tracking the files
        for root, _, files in os.walk(self.directory):
            for file in files:
                if file.endswith(".txt"):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            file_content = f.read()

                        candidates = get_initialism_candidates(
                            self.initialism, file_content, stopwords
                        )

                        for candidate in candidates:
                            if candidate not in candidates_with_sources:
                                candidates_with_sources[candidate] = []
                            candidates_with_sources[candidate].append(file_path)

                    except Exception as e:
                        print(f"Error reading file {file_path}: {e}")

        return candidates_with_sources
