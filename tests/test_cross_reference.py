from src.cross_reference import (
    cross_reference_extensions,
    generate_cross_reference_summary,
)


def test_cross_reference_basic_matching():
    """
    Test correct extension matching.
    """

    json_extensions = {"i", "m", "zba"}
    manual_extensions = {"i", "m", "zbb"}

    results = cross_reference_extensions(
        json_extensions,
        manual_extensions
    )

    assert results["matched"] == {"i", "m"}
    assert results["json_only"] == {"zba"}
    assert results["manual_only"] == {"zbb"}


def test_cross_reference_empty_sets():
    """
    Test empty inputs produce empty outputs.
    """

    results = cross_reference_extensions(set(), set())

    assert results["matched"] == set()
    assert results["json_only"] == set()
    assert results["manual_only"] == set()


def test_generate_cross_reference_summary():
    """
    Test formatted summary generation.
    """

    sample_results = {
        "matched": {"i", "m"},
        "json_only": {"zba"},
        "manual_only": {"zbb", "f"},
    }

    summary = generate_cross_reference_summary(sample_results)

    assert summary == [
        "Matched extensions: 2",
        "Extensions only in instr_dict.json: 1",
        "Extensions only in ISA manual: 2",
    ]
