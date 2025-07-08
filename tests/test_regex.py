import pytest

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
