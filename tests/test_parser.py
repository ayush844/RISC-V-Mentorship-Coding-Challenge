import json
import pytest

from src.parser import load_instruction_data


def test_load_valid_instruction_data(tmp_path):
    """
    Test that valid JSON instruction data loads correctly.
    """

    sample_data = {
        "add": {
            "extension": ["rv_i"]
        }
    }

    test_file = tmp_path / "valid_instr.json"
    test_file.write_text(json.dumps(sample_data), encoding="utf-8")

    loaded_data = load_instruction_data(test_file)

    assert loaded_data == sample_data


def test_missing_file_raises_error():
    """
    Test that missing files raise FileNotFoundError.
    """

    with pytest.raises(FileNotFoundError):
        load_instruction_data("non_existent_file.json")


def test_invalid_json_raises_value_error(tmp_path):
    """
    Test malformed JSON raises ValueError.
    """

    test_file = tmp_path / "invalid.json"
    test_file.write_text("{invalid json}", encoding="utf-8")

    with pytest.raises(ValueError, match="Invalid JSON format"):
        load_instruction_data(test_file)


def test_invalid_root_structure_raises_value_error(tmp_path):
    """
    Test non-dictionary JSON root raises ValueError.
    """

    invalid_data = ["not", "a", "dictionary"]

    test_file = tmp_path / "invalid_structure.json"
    test_file.write_text(json.dumps(invalid_data), encoding="utf-8")

    with pytest.raises(ValueError, match="Invalid JSON structure"):
        load_instruction_data(test_file)