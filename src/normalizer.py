import re


def normalize_extension_name(extension_name):
    """
    Normalize extension names from JSON or ISA manual into
    a canonical lowercase format.

    Examples:
        rv_i -> i
        rv64_zba -> zba
        Zba -> zba
        M -> m

    Args:
        extension_name (str):
            Raw extension name.

    Returns:
        str:
            Normalized extension name.
    """

    if not extension_name:
        return ""

    # Normalize case and whitespace
    normalized = extension_name.strip().lower()

    # Remove rv, rv32, rv64 prefixes
    normalized = re.sub(r"^rv(32|64)?_", "", normalized)

    return normalized