import json
from pathlib import Path


def load_instruction_data(file_path):
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format in file: {file_path}") from e
    
    if not isinstance(data, dict):
        raise ValueError(f"Invalid JSON structure: expected dictionary in file: {file_path}")
    
    return data