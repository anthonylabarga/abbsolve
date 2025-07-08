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
            (sub / f"doc{j}.txt").write_text(f"This is document {j} in subdirectory {i}.")


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
