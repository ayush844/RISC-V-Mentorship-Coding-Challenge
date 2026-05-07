import re
from pathlib import Path

from src.normalizer import normalize_extension_name


def extract_manual_extensions(manual_src_path):
    """
    Scan RISC-V ISA manual AsciiDoc files for extension references.

    Args:
        manual_src_path (str or Path):
            Path to riscv-isa-manual/src directory.

    Returns:
        set:
            Normalized extension names found in manual.
    """

    manual_src_path = Path(manual_src_path)

    if not manual_src_path.exists():
        raise FileNotFoundError(
            f"Manual source path not found: {manual_src_path}"
        )

    extension_set = set()

    # Regex patterns
    z_extension_pattern = re.compile(r"\bZ[a-zA-Z0-9]+\b") # Z extensions: Zba, Zbb, Zicsr, etc.
    base_extension_pattern = re.compile(r"\b[IMAFDCHQ]\b") # Single-letter base extensions: I, M, A, F, D, C, H, Q

    # Scan all .adoc files recursively
    for adoc_file in manual_src_path.rglob("*.adoc"):

        try:
            content = adoc_file.read_text(
                encoding="utf-8",
                errors="ignore"
            )
        except Exception:
            continue

        # Find Z-style extensions
        z_matches = z_extension_pattern.findall(content)

        # Find base single-letter extensions
        base_matches = base_extension_pattern.findall(content)

        all_matches = z_matches + base_matches

        for match in all_matches:
            normalized = normalize_extension_name(match)

            if normalized:
                extension_set.add(normalized)

    return extension_set