def cross_reference_extensions(json_extensions, manual_extensions):
    """
    Compare normalized JSON extensions against ISA manual extensions.

    Args:
        json_extensions (set):
            Extensions from instr_dict.json

        manual_extensions (set):
            Extensions from ISA manual

    Returns:
        dict:
            Contains matched, json_only, and manual_only sets.
    """

    matched = json_extensions & manual_extensions
    json_only = json_extensions - manual_extensions
    manual_only = manual_extensions - json_extensions

    return {
        "matched": matched,
        "json_only": json_only,
        "manual_only": manual_only,
    }


def generate_cross_reference_summary(cross_ref_results):
    """
    Generate formatted summary lines for Tier 2 report.

    Args:
        cross_ref_results (dict):
            Cross-reference result dictionary.

    Returns:
        list:
            Summary lines.
    """

    matched_count = len(cross_ref_results["matched"])
    json_only_count = len(cross_ref_results["json_only"])
    manual_only_count = len(cross_ref_results["manual_only"])

    summary_lines = [
        f"Matched extensions: {matched_count}",
        f"Extensions only in instr_dict.json: {json_only_count}",
        f"Extensions only in ISA manual: {manual_only_count}",
    ]

    return summary_lines