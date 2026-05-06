from parser import load_instruction_data

from tier1 import process_tier1, generate_summary


def main():

    # Path to the RISC-V instruction dataset
    file_path = 'data/instr_dict.json'

    try:
        # Load and validate instruction JSON data
        instruction_data = load_instruction_data(file_path)

        print("Instruction data loaded successfully:")
        print(f"Total instructions loaded: {len(instruction_data)}")

        # Tier 1 core processing:
        # - Group instructions by extension
        # - Detect instructions belonging to multiple extensions
        grouped_extensions, multi_extension_instructions = process_tier1(
            instruction_data
        )

        # Generate formatted extension summary lines
        summary_lines = generate_summary(grouped_extensions)

        print("\n------------- Extension Summary -------------")
        for line in summary_lines[:20]:
            print(line)

        print("\n------------- Instructions in Multiple Extensions -------------")
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

    except Exception as e:
        print(f"Error loading instruction data: {e}")
        return
    
if __name__ == "__main__":
    main()
