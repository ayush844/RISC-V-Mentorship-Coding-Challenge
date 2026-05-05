from collections import defaultdict


def process_tier1(instruction_data):
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