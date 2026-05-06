from src.tier1 import process_tier1, generate_summary


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

    assert summary == [
        "rv_i | 2 instructions | e.g. add",
        "rv_m | 1 instructions | e.g. mul"
    ]


def test_generate_summary_sorted_extensions():
    """
    Test extensions are sorted alphabetically.
    """

    grouped_extensions = {
        "rv_z": {"zinst"},
        "rv_a": {"ainst"}
    }

    summary = generate_summary(grouped_extensions)

    assert summary[0].startswith("rv_a")
    assert summary[1].startswith("rv_z")