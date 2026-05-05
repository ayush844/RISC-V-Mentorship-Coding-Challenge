from parser import load_instruction_data


def main():
    file_path = 'data/instr_dict.json'

    try:
        instruction_data = load_instruction_data(file_path)

        print("Instruction data loaded successfully:")
        print(f"Total instructions loaded: {len(instruction_data)}")

        print("\nSample instruction data:")
        for i, (mnemonic, metadata) in enumerate(instruction_data.items()):
            if i >= 10:
                break
            print(f"{mnemonic}: {metadata.get('extension', [])}")

    except Exception as e:
        print(f"Error loading instruction data: {e}")
        return
    
if __name__ == "__main__":
    main()
