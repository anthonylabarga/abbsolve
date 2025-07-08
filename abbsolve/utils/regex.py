"""
Helper functions for finding patterns in large text corpora with regular expressions.
"""

import re
from typing import List, Set


def get_initialism_candidates(
        initialism: str, text_to_search: str, stopwords: List[str] | None = None
) -> Set[str]:
    """
    Given an initialism, returns

    Args:
        initialism: the initialism to be inverted, will be stripped of punctuation and made lowercase
        text_to_search: the string to search for inversion candidates
        stopwords: a set of stopwords that are allowed to interpose the n-grams, defaults to common English stopwords
        unless the user brings their own

    Returns: a set of n-grams whose first letters map to the elements of the initialism
    """

    if not initialism or not text_to_search:
        return set()

    # set standard stopwords if the user didn't bring their own
    if stopwords is None:
        stopwords = [
            "of",
            "the",
            "a",
            "an",
            "for",
            "in",
            "on",
            "to",
            "with",
            "by",
            "and",
        ]

    # filter out punctuation and convert to lowercase
    initialism = re.sub(r"[\W_]+", "", initialism).lower()

    # regular expression to match n-grams whose terms start with the same letters as the initialism
    stopword_pattern = r"(?:" + "|".join(stopwords) + r")"
    pattern = r"\b" + rf"\w*(?:\s+{stopword_pattern}){{0,2}}?\s+".join(
        [f"{char}\w*" for char in initialism]
    )

    # run case-insensitive regex and get all candidates
    matches = re.findall(pattern, text_to_search, re.IGNORECASE)

    return set(matches)
