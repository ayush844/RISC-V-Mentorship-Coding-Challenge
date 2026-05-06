from collections import defaultdict


def process_tier1(instruction_data):
    """
    Process instruction data for Tier 1 requirements.

    Groups instructions by extension and identifies instructions
    that belong to multiple extensions.

    Args:
        instruction_data (dict):
            Parsed instruction dictionary.

    Returns:
        tuple:
            grouped_extensions (defaultdict(set)):
                Maps extension tags to instruction mnemonics.

            multi_extension_instructions (dict):
                Maps mnemonics to multiple extensions.
    """

    grouped_extensions = defaultdict(set)
    multi_extension_instructions = {}

    for mnemonic, metadata in instruction_data.items():
        extensions = metadata.get("extension", [])

        if isinstance(extensions, str):
            extensions = [extensions]
        
        if not extensions:
            continue

        for ext in extensions:
            grouped_extensions[ext].add(mnemonic)
        
        if len(extensions) > 1:
            multi_extension_instructions[mnemonic] = extensions
        
    return grouped_extensions, multi_extension_instructions


def generate_summary(grouped_extensions):
    """
    Generate formatted Tier 1 summary lines.

    Args:
        grouped_extensions (dict):
            Maps extension tags to instruction mnemonics.

    Returns:
        list:
            Formatted summary lines.
    """

    summary_lines = []

    for extension in sorted(grouped_extensions.keys()):
        instructions = sorted(grouped_extensions[extension])
        instruction_count = len(instructions)
        example_mnemonic = instructions[0] if instructions else "N/A"

        summary_line = (
            f"{extension} | "
            f"{instruction_count} instructions | "
            f"e.g. {example_mnemonic}"
        )

        summary_lines.append(summary_line)

    return summary_lines