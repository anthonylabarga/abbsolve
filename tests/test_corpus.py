"""
Tests for the corpus reader.
"""

from abbsolve.documents.corpus import txt_generator


def test_read_txt_corpus(tmp_path):
    """
    Uses pytest's tmp_path fixture to create a temporary directory structure
    """

    d = tmp_path / "corpus"
    d.mkdir()

    # make fifty docs in the tmp_path directory
    for i in range(50):
        (d / f"doc{i}.txt").write_text(f"This is document {i}.")

    # make ten subdirectories, each with five documents
    for i in range(10):
        sub = d / f"subdir{i}"
        sub.mkdir()
        for j in range(5):
            (sub / f"doc{j}.txt").write_text(
                f"This is document {j} in subdirectory {i}."
            )

    # test that log, markdown, PDF, and .docx files are ignored
    (d / "doc1.log").write_text("This is a log file.")
    (d / "doc2.md").write_text("This is a markdown file.")
    (d / "doc3.pdf").write_text("This is a PDF file.")
    (d / "doc4.docx").write_text("This is a Word document.")

    docs = list(txt_generator(str(d)))

    assert len(docs) == 100

    for i in range(50):
        assert f"This is document {i}." in docs

    for i in range(10):
        for j in range(5):
            assert f"This is document {j} in subdirectory {i}." in docs


def test_txt_generator_exception_handling(tmp_path, capsys):
    """
    Tests that the txt_generator handles file read errors gracefully by
    creating a file with an invalid UTF-8 sequence.
    """
    d = tmp_path / "corpus"
    d.mkdir()

    # Create a file that will cause a UnicodeDecodeError
    error_file_path = d / "error.txt"
    error_file_path.write_bytes(b"\x80abc")

    # Create a valid file to ensure the generator continues after the error
    (d / "good.txt").write_text("This is a good file.")

    # Consume the generator to trigger the read attempts
    docs = list(txt_generator(str(d)))

    # Check that only the valid file's content was yielded
    assert len(docs) == 1
    assert docs[0] == "This is a good file."

    # Check that the error message was printed to standard output
    captured = capsys.readouterr()
    assert "Error reading file" in captured.out
    assert str(error_file_path) in captured.out
