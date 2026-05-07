from src.tier1 import (process_tier1, generate_summary,
                       format_multi_extension_table)


def test_process_tier1_single_extension_grouping():
    """
    Test instructions are correctly grouped under single extensions.
    """

    sample_data = {
        "add": {"extension": ["rv_i"]},
        "mul": {"extension": ["rv_m"]}
    }

    grouped_extensions, multi_extension_instructions = process_tier1(sample_data)

    assert grouped_extensions["rv_i"] == {"add"}
    assert grouped_extensions["rv_m"] == {"mul"}

    assert multi_extension_instructions == {}


def test_process_tier1_multi_extension_detection():
    """
    Test instructions with multiple extensions are detected correctly.
    """

    sample_data = {
        "foo": {"extension": ["rv_i", "rv_m"]}
    }

    grouped_extensions, multi_extension_instructions = process_tier1(sample_data)

    assert grouped_extensions["rv_i"] == {"foo"}
    assert grouped_extensions["rv_m"] == {"foo"}

    assert multi_extension_instructions["foo"] == ["rv_i", "rv_m"]


def test_process_tier1_string_extension_normalization():
    """
    Test string extension values are normalized into lists.
    """

    sample_data = {
        "add": {"extension": "rv_i"}
    }

    grouped_extensions, _ = process_tier1(sample_data)

    assert grouped_extensions["rv_i"] == {"add"}


def test_process_tier1_skips_empty_extensions():
    """
    Test instructions with empty or missing extensions are skipped.
    """

    sample_data = {
        "invalid1": {"extension": []},
        "invalid2": {},
        "valid": {"extension": ["rv_i"]}
    }

    grouped_extensions, multi_extension_instructions = process_tier1(sample_data)

    assert grouped_extensions["rv_i"] == {"valid"}

    assert "invalid1" not in grouped_extensions
    assert "invalid2" not in grouped_extensions

    assert multi_extension_instructions == {}


def test_generate_summary_format():
    """
    Test summary output formatting is correct.
    """

    grouped_extensions = {
        "rv_i": {"add", "addi"},
        "rv_m": {"mul"}
    }

    summary = generate_summary(grouped_extensions)

    # Check header
    assert summary[0].startswith("Extension")
    assert "Count" in summary[0]

    # Check separator
    assert set(summary[1]) == {"-"}

    # Check number of lines (header + separator + 2 entries)
    assert len(summary) == 4

    # Check content lines (ignore spacing issues)
    assert "rv_i" in summary[2]
    assert "2" in summary[2]
    assert "add" in summary[2]

    assert "rv_m" in summary[3]
    assert "1" in summary[3]
    assert "mul" in summary[3]


def test_generate_summary_sorted_extensions():
    """
    Test extensions are sorted alphabetically.
    """

    grouped_extensions = {
        "rv_z": {"zinst"},
        "rv_a": {"ainst"}
    }

    summary = generate_summary(grouped_extensions)

    # Skip header + separator
    data_lines = summary[2:]

    assert data_lines[0].strip().startswith("rv_a")
    assert data_lines[1].strip().startswith("rv_z")


def test_format_multi_extension_table():
    """
    Test formatting of multi-extension instruction table.
    """

    sample = {
        "foo": ["rv_i", "rv_m"],
        "bar": ["rv_zba", "rv_zbb"]
    }

    lines = format_multi_extension_table(sample)

    # Header
    assert lines[0].startswith("Instruction")

    # Separator
    assert set(lines[1]) == {"-"}

    # Extract data rows (ignore header)
    data_lines = lines[2:]

    # Combine into one string for easier checking
    joined = "\n".join(data_lines)

    assert "foo" in joined
    assert "rv_i" in joined
    assert "rv_m" in joined

    assert "bar" in joined
    assert "rv_zba" in joined
    assert "rv_zbb" in joined
