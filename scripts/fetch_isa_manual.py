import shutil
import subprocess
from pathlib import Path


def fetch_isa_manual(dest_path="data/riscv-isa-manual-src"):
    """
    Fetch RISC-V ISA manual source files (only src/ directory).

    - Clones official repo temporarily
    - Copies src/ into project data folder
    - Cleans up temporary clone

    Args:
        dest_path (str): Destination path for src files
    """

    dest_path = Path(dest_path)

    # If already exists, skip fetching
    if dest_path.exists():
        print("ISA manual source already exists. Skipping fetch.")
        return

    print("Fetching RISC-V ISA manual repository...")

    temp_dir = Path("temp_riscv_manual")

    try:
        # Clone repo shallow (faster)
        subprocess.run(
            ["git", "clone", "--depth", "1",
             "https://github.com/riscv/riscv-isa-manual.git",
             str(temp_dir)],
            check=True
        )

        src_path = temp_dir / "src"

        if not src_path.exists():
            raise FileNotFoundError("src/ folder not found in cloned repo")

        # Copy only src/ directory
        shutil.copytree(src_path, dest_path)

        print(f"ISA manual src copied to: {dest_path}")

    finally:
        # Clean up temp repo
        if temp_dir.exists():
            shutil.rmtree(temp_dir)

        print("Temporary files cleaned up.")