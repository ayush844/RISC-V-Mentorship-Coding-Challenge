from src.instruction_parser import load_instruction_data

from src.tier1 import process_tier1, generate_summary
from src.normalizer import normalize_extension_name
from src.manual_parser import extract_manual_extensions
from src.cross_reference import (
    cross_reference_extensions,
    generate_cross_reference_summary,
)
from scripts.fetch_isa_manual import fetch_isa_manual
from pathlib import Path


def main():

    # Path to Tier 1 instruction dataset JSON file
    file_path = 'data/instr_dict.json'

    # Path to ISA manual source files (only src/ directory)
    manual_src_path = "data/riscv-isa-manual-src"

    try:
        # Load and validate instruction JSON data
        instruction_data = load_instruction_data(file_path)

        print("Instruction data loaded successfully:")
        print(f"Total instructions loaded: {len(instruction_data)}")

        # Tier 1 processing:
        # - Group instructions by extension
        # - Detect instructions belonging to multiple extensions
        grouped_extensions, multi_extension_instructions = process_tier1(
            instruction_data
        )

        # Generate formatted extension summary lines
        summary_lines = generate_summary(grouped_extensions)

        print("\n------------- Tier 1: Extension Summary -------------")
        for line in summary_lines[:20]:
            print(line)

        print("\n------------- Tier 1: Instructions in Multiple Extensions -------------")
        for mnemonic, extensions in list(multi_extension_instructions.items())[:20]:
            print(f"{mnemonic} | {', '.join(extensions)}")

        # Output file path for Tier 1 results
        output_path = "output/tier1_summary.txt"

        # Save complete Tier 1 report to output file
        with open(output_path, "w", encoding="utf-8") as output_file:

            # Write extension summary section
            output_file.write("------------- Extension Summary -------------\n")

            for line in summary_lines:
                output_file.write(line + "\n")

            # Write multi-extension section header
            output_file.write(
                "\n------------- Instructions in Multiple Extensions -------------\n"
            )

            for mnemonic, extensions in sorted(
                multi_extension_instructions.items()
            ):
                output_file.write(
                    f"{mnemonic} | {', '.join(extensions)}\n"
                )

        print(f"\nTier 1 output saved to: {output_path}")

        # Tier 2 Processing

        # Ensure ISA manual data exists before Tier 2
        manual_src_path = Path(manual_src_path)

        if not manual_src_path.exists():
            print("\nISA manual source not found. Fetching automatically...")
            fetch_isa_manual(manual_src_path)
            if not manual_src_path.exists():
                raise RuntimeError("Failed to fetch ISA manual source files.")

        # Normalize JSON extensions from Tier 1
        json_extensions = {
            normalize_extension_name(ext)
            for ext in grouped_extensions.keys()
        }

        # Extract extensions from ISA manual source files
        manual_extensions = extract_manual_extensions(manual_src_path)

        # Cross-reference both extension sets
        cross_ref_results = cross_reference_extensions(
            json_extensions,
            manual_extensions
        )

        # Generate Tier 2 summary
        tier2_summary = generate_cross_reference_summary(
            cross_ref_results
        )

        # Display Tier 2 summary
        print(
            "\n------------- Tier 2: Cross-Reference Summary -------------"
        )

        for line in tier2_summary:
            print(line)

        # Display JSON-only extensions
        print(
            "\n------------- Extensions Only in instr_dict.json -------------"
        )

        for ext in sorted(cross_ref_results["json_only"]):
            print(ext)

        # Display manual-only extensions
        print(
            "\n------------- Extensions Only in ISA Manual -------------"
        )

        for ext in sorted(cross_ref_results["manual_only"]):
            print(ext)

        # Save Tier 2 report
        tier2_output_path = "output/tier2_cross_reference.txt"

        with open(tier2_output_path, "w", encoding="utf-8") as output_file:

            output_file.write(
                "------------- Tier 2: Cross-Reference Summary -------------\n"
            )

            for line in tier2_summary:
                output_file.write(line + "\n")

            output_file.write(
                "\n------------- Extensions Only in instr_dict.json -------------\n"
            )

            for ext in sorted(cross_ref_results["json_only"]):
                output_file.write(ext + "\n")

            output_file.write(
                "\n------------- Extensions Only in ISA Manual -------------\n"
            )

            for ext in sorted(cross_ref_results["manual_only"]):
                output_file.write(ext + "\n")

        print(f"\nTier 2 output saved to: {tier2_output_path}")

    except Exception as e:
        print(f"Error loading instruction data: {e}")
        return
    
if __name__ == "__main__":
    main()
