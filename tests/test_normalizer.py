from src.normalizer import normalize_extension_name


def test_normalize_basic_rv_extension():
    """
    Test standard rv_ prefix removal.
    """

    assert normalize_extension_name("rv_i") == "i"
    assert normalize_extension_name("rv_m") == "m"


def test_normalize_rv32_rv64_extensions():
    """
    Test rv32_ and rv64_ prefix removal.
    """

    assert normalize_extension_name("rv32_zba") == "zba"
    assert normalize_extension_name("rv64_zbb") == "zbb"


def test_normalize_manual_extension_names():
    """
    Test ISA manual naming normalization.
    """

    assert normalize_extension_name("Zba") == "zba"
    assert normalize_extension_name("M") == "m"


def test_normalize_whitespace_and_case():
    """
    Test whitespace trimming and lowercase conversion.
    """

    assert normalize_extension_name("  RV64_ZBA ") == "zba"


def test_normalize_empty_input():
    """
    Test empty or invalid input handling.
    """

    assert normalize_extension_name("") == ""
    assert normalize_extension_name(None) == ""