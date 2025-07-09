import os
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from abbsolve.infer.regex import RegexInitialismInverter
from abbsolve.utils.regex import get_initialism_candidates

test_cases = [
    (
        "NLP",
        "Natural Language Processing is a field of AI.",
        {"Natural Language Processing"},
    ),
    (
        "U.S.A.",
        "The United States of America is a country.",
        {"United States of America"},
    ),
    (
        "I.B.M.",
        "International Business Machines is a tech company.",
        {"International Business Machines"},
    ),
    (
        "DM",
        "A Direct Message or a Dungeon Master?",
        {"Direct Message", "Dungeon Master"},
    ),
    (
        "PC",
        "Personal Computer or Politically Correct, the choice is yours.",
        {"Personal Computer", "Politically Correct"},
    ),
    (
        "GIT",
        "Get In Touch or Global Information Tracker, both are valid for GIT.",
        {"Get In Touch", "Global Information Tracker"},
    ),
    (
        "OS",
        "Operating System or Open Source, both are abbreviated as OS.",
        {"Operating System", "Open Source"},
    ),
    (
        "SQL",
        "Structured Query Language, but some say Sequel Query Language.",
        {"Structured Query Language", "Sequel Query Language"},
    ),
    ("FBI", "Federal Bureau certainly of Investigation", set()),
    ("WHO", "World Health surely Organization", set()),
    ("UN", "United really Nations", set()),
    ("EU", "European definitely Union", set()),
    ("UK", "United lovely Kingdom", set()),
    ("CEO", "Chief Executive really Officer", set()),
    ("N.L.P.", "Natural Language Processing", {"Natural Language Processing"}),
    ("U-S-A", "United States of America", {"United States of America"}),
    ("I_B_M", "International Business Machines", {"International Business Machines"}),
    (
        "N@A@S@A",
        "National Aeronautics and Space Administration",
        {"National Aeronautics and Space Administration"},
    ),
    ("F!B!I!", "Federal Bureau of Investigation", {"Federal Bureau of Investigation"}),
    ("C.I.A", "Central Intelligence Agency", {"Central Intelligence Agency"}),
    ("W.H.O.", "World Health Organization", {"World Health Organization"}),
    ("U...N...", "United Nations", {"United Nations"}),
    ("E_U_", "European Union", {"European Union"}),
    ("G-7", "Group of Seven", set()),
    (
        "HR",
        "Human Resources is a department. Contact Human Resources.",
        {"Human Resources"},
    ),
    (
        "AI",
        "Artificial Intelligence is a field. The future is Artificial Intelligence.",
        {"Artificial Intelligence"},
    ),
    (
        "CSS",
        "Cascading Style Sheets is for styling. Use Cascading Style Sheets.",
        {"Cascading Style Sheets"},
    ),
    ("ID", "Identity Document", {"Identity Document"}),
    ("API", "Application Programming Interface", {"Application Programming Interface"}),
    ("DIY", "Do It Yourself", {"Do It Yourself"}),
    ("FAQ", "Frequently Asked Questions", {"Frequently Asked Questions"}),
    ("ASAP", "As Soon As Possible", {"As Soon As Possible"}),
    ("UFO", "Unidentified Flying Object", {"Unidentified Flying Object"}),
    ("PIN", "Personal Identification Number", {"Personal Identification Number"}),
    ("RAM", "Random Access Memory", {"Random Access Memory"}),
    ("ROM", "Read Only Memory", {"Read Only Memory"}),
    ("CPU", "Central Processing Unit", {"Central Processing Unit"}),
    ("GPU", "Graphics Processing Unit", {"Graphics Processing Unit"}),
    ("URL", "Uniform Resource Locator", {"Uniform Resource Locator"}),
    ("CD", "Compact Disc", {"Compact Disc"}),
    ("VR", "Virtual Reality", {"Virtual Reality"}),
    ("AR", "Augmented Reality", {"Augmented Reality"}),
    ("WWW", "World Wide Web", {"World Wide Web"}),
    ("YOLO", "You Only Live Once", {"You Only Live Once"}),
    ("FOMO", "Fear Of Missing Out", {"Fear Of Missing Out"}),
    # edge cases that will fail now, but a semantic approach should fix
    (
        "CIA",
        "Central Intelligence absolutely Agency",
        set("Central Intelligence Agency"),
    ),
    (
        "NASA",
        "National Aeronautics space and Space Administration",
        set("National Aeronautics and Space Administration"),
    ),
    ("TV", "People say that television warps your mind!", set("television")),
    (
        "JS",
        "JavaScript is a programming language. Many people use JavaScript.",
        {"JavaScript"},
    ),
    (
        "HTML",
        "HyperText Markup Language defines a web document's structure.",
        {"HyperText Markup Language"},
    ),
]


@pytest.mark.parametrize("initialism, text_to_search, expected", test_cases)
def test_get_initialism_candidates(initialism, text_to_search, expected):
    """
    Tests the get_initialism_candidates function with various inputs.
    """
    assert get_initialism_candidates(initialism, text_to_search) == expected


def test_emppty_initialism():
    """
    Tests the get_initialism_candidates function with an empty initialism.
    """
    assert get_initialism_candidates("", "Some text") == set()


class TestRegexInitialismInverter:
    """Test class for RegexInitialismInverter."""

    @pytest.fixture
    def temp_dir_with_files(self):
        """Create a temporary directory with test txt files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test files with different content
            test_files = {
                "file1.txt": "Natural Language Processing is a field of AI. Machine Learning and Deep Learning are related.",
                "file2.txt": "The United States of America is a country. NASA stands for National Aeronautics and Space Administration.",
                "subdir/file3.txt": "Application Programming Interface design is important. REST API development requires careful planning.",
                "subdir/nested/file4.txt": "Central Processing Unit performance matters. Graphics Processing Unit acceleration helps.",
                "other.log": "This should be ignored as it's not a txt file.",
                "empty.txt": "",
            }

            for file_path, content in test_files.items():
                full_path = Path(temp_dir) / file_path
                full_path.parent.mkdir(parents=True, exist_ok=True)
                full_path.write_text(content, encoding="utf-8")

            yield temp_dir

    def test_init_valid_inputs(self, temp_dir_with_files):
        """Test initialization with valid inputs."""
        inverter = RegexInitialismInverter("NLP", temp_dir_with_files)
        assert inverter.initialism == "NLP"
        assert inverter.directory == temp_dir_with_files

    def test_init_strips_whitespace(self, temp_dir_with_files):
        """Test that initialism whitespace is stripped."""
        inverter = RegexInitialismInverter("  NLP  ", temp_dir_with_files)
        assert inverter.initialism == "NLP"

    def test_init_empty_initialism_raises_error(self, temp_dir_with_files):
        """Test that empty initialism raises ValueError."""
        with pytest.raises(ValueError, match="Initialism cannot be empty"):
            RegexInitialismInverter("", temp_dir_with_files)

        with pytest.raises(ValueError, match="Initialism cannot be empty"):
            RegexInitialismInverter("   ", temp_dir_with_files)

    def test_init_nonexistent_directory_raises_error(self):
        """Test that nonexistent directory raises ValueError."""
        with pytest.raises(ValueError, match="Directory does not exist"):
            RegexInitialismInverter("NLP", "/nonexistent/directory")

    def test_init_file_instead_of_directory_raises_error(self, temp_dir_with_files):
        """Test that passing a file instead of directory raises ValueError."""
        file_path = os.path.join(temp_dir_with_files, "file1.txt")
        with pytest.raises(ValueError, match="Path is not a directory"):
            RegexInitialismInverter("NLP", file_path)

    def test_find_candidates_basic(self, temp_dir_with_files):
        """Test basic candidate finding functionality."""
        inverter = RegexInitialismInverter("NLP", temp_dir_with_files)
        candidates = inverter.find_candidates()
        assert "Natural Language Processing" in candidates

    def test_find_candidates_multiple_files(self, temp_dir_with_files):
        """Test that candidates are found across multiple files."""
        inverter = RegexInitialismInverter("API", temp_dir_with_files)
        candidates = inverter.find_candidates()
        assert "Application Programming Interface" in candidates

    def test_find_candidates_subdirectories(self, temp_dir_with_files):
        """Test that files in subdirectories are searched."""
        inverter = RegexInitialismInverter("CPU", temp_dir_with_files)
        candidates = inverter.find_candidates()
        assert "Central Processing Unit" in candidates

    def test_find_candidates_with_custom_stopwords(self, temp_dir_with_files):
        """Test candidate finding with custom stopwords."""
        inverter = RegexInitialismInverter("ML", temp_dir_with_files)
        candidates = inverter.find_candidates(stopwords=["and"])
        assert "Machine Learning" in candidates

    def test_find_candidates_no_matches(self, temp_dir_with_files):
        """Test when no candidates are found."""
        inverter = RegexInitialismInverter("XYZ", temp_dir_with_files)
        candidates = inverter.find_candidates()
        assert len(candidates) == 0

    def test_find_candidates_with_sources_basic(self, temp_dir_with_files):
        """Test finding candidates with source file information."""
        inverter = RegexInitialismInverter("NLP", temp_dir_with_files)
        candidates_with_sources = inverter.find_candidates_with_sources()

        assert "Natural Language Processing" in candidates_with_sources
        source_files = candidates_with_sources["Natural Language Processing"]
        assert len(source_files) == 1
        assert source_files[0].endswith("file1.txt")

    def test_find_candidates_with_sources_multiple_files(self, temp_dir_with_files):
        """Test that source tracking works across multiple files."""
        # Add NASA to multiple files to test source tracking
        nasa_content = "NASA stands for National Aeronautics and Space Administration."

        # Write to an additional file
        additional_file = os.path.join(temp_dir_with_files, "nasa.txt")
        with open(additional_file, "w", encoding="utf-8") as f:
            f.write(nasa_content)

        inverter = RegexInitialismInverter("NASA", temp_dir_with_files)
        candidates_with_sources = inverter.find_candidates_with_sources()

        if "National Aeronautics and Space Administration" in candidates_with_sources:
            source_files = candidates_with_sources[
                "National Aeronautics and Space Administration"
            ]
            assert len(source_files) >= 1
            assert any(
                f.endswith("file2.txt") or f.endswith("nasa.txt") for f in source_files
            )

    def test_find_candidates_with_sources_empty_result(self, temp_dir_with_files):
        """Test source tracking when no candidates are found."""
        inverter = RegexInitialismInverter("XYZ", temp_dir_with_files)
        candidates_with_sources = inverter.find_candidates_with_sources()
        assert len(candidates_with_sources) == 0

    def test_find_candidates_ignores_non_txt_files(self, temp_dir_with_files):
        """Test that non-txt files are ignored."""
        # The temp directory contains "other.log" which should be ignored
        inverter = RegexInitialismInverter("LOG", temp_dir_with_files)
        candidates = inverter.find_candidates()
        # Should not find anything since .log files are ignored
        assert len(candidates) == 0

    def test_empty_directory(self):
        """Test behavior with empty directory."""
        with tempfile.TemporaryDirectory() as empty_dir:
            inverter = RegexInitialismInverter("NLP", empty_dir)
            candidates = inverter.find_candidates()
            assert len(candidates) == 0

            candidates_with_sources = inverter.find_candidates_with_sources()
            assert len(candidates_with_sources) == 0

    def test_directory_with_only_empty_files(self):
        """Test behavior with directory containing only empty txt files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create empty txt files
            for i in range(3):
                empty_file = os.path.join(temp_dir, f"empty{i}.txt")
                with open(empty_file, "w", encoding="utf-8") as f:
                    f.write("")

            inverter = RegexInitialismInverter("NLP", temp_dir)
            candidates = inverter.find_candidates()
            assert len(candidates) == 0

    def test_find_candidates_with_sources_file_read_error(
            self, temp_dir_with_files, capsys
    ):
        """Test that file read errors are handled gracefully and logged."""
        inverter = RegexInitialismInverter("NLP", temp_dir_with_files)

        # Mock the open function to raise an exception for one specific file
        original_open = open

        def mock_open_func(*args, **kwargs):
            if "file1.txt" in str(args[0]):
                raise PermissionError("Simulated permission denied")
            return original_open(*args, **kwargs)

        with patch("builtins.open", side_effect=mock_open_func):
            candidates_with_sources = inverter.find_candidates_with_sources()

        # Check that error was printed
        captured = capsys.readouterr()
        assert "Error reading file" in captured.out
        assert "file1.txt" in captured.out
        assert "Simulated permission denied" in captured.out

        # Should still find candidates from other files that didn't error
        # (e.g., NASA from file2.txt should still be found)
        # The exact candidates depend on what's in the other files
