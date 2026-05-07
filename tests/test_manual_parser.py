from pathlib import Path
import pytest

from src.manual_parser import extract_manual_extensions


def test_extract_manual_extensions_basic(tmp_path):
    """
    Test extraction of extensions from sample AsciiDoc files.
    """

    # Create sample AsciiDoc file
    adoc_file = tmp_path / "sample.adoc"

    adoc_file.write_text(
        """
        The Zba extension improves address generation.
        The M extension provides multiplication.
        Zicsr handles control and status registers.
        """,
        encoding="utf-8"
    )

    extensions = extract_manual_extensions(tmp_path)

    assert "zba" in extensions
    assert "m" in extensions
    assert "zicsr" in extensions


def test_extract_manual_extensions_empty_directory(tmp_path):
    """
    Test empty directory returns empty set.
    """

    extensions = extract_manual_extensions(tmp_path)

    assert extensions == set()


def test_extract_manual_extensions_missing_path():
    """
    Test missing path raises FileNotFoundError.
    """

    with pytest.raises(FileNotFoundError):
        extract_manual_extensions("non_existent_directory")


def test_extract_manual_extensions_multiple_files(tmp_path):
    """
    Test parser scans multiple AsciiDoc files recursively.
    """

    file1 = tmp_path / "file1.adoc"
    file2 = tmp_path / "file2.adoc"

    file1.write_text("Zbb extension", encoding="utf-8")
    file2.write_text("F extension", encoding="utf-8")

    extensions = extract_manual_extensions(tmp_path)

    assert "zbb" in extensions
    assert "f" in extensions