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

    header = f"{'Extension':<15} | {'Count':<6} | Example"
    separator = "-" * 45

    summary_lines = [header, separator]

    for extension in sorted(grouped_extensions.keys()):
        instructions = sorted(grouped_extensions[extension])
        count = len(instructions)
        example = instructions[0] if instructions else "N/A"

        line = f"{extension:<15} | {count:<6} | {example}"
        summary_lines.append(line)

    return summary_lines


def format_multi_extension_table(multi_extension_instructions):
    """
    Generate table for instructions belonging to multiple extensions.
    """

    header = f"{'Instruction':<15} | Extensions"
    separator = "-" * 50

    lines = [header, separator]

    for mnemonic, extensions in sorted(multi_extension_instructions.items()):
        ext_str = ", ".join(sorted(extensions))
        line = f"{mnemonic:<15} | {ext_str}"
        lines.append(line)

    return lines
