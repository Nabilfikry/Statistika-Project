"""
Orchestrator: Menjalankan seluruh pipeline analisis statistika.
"""

import subprocess
import sys
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
NOTEBOOKS_DIR = BASE_DIR / "notebooks"


def clean_outputs(base_dir: Path) -> None:
    """Membersihkan output lama sebelum eksekusi."""
    processed_file = base_dir / "dataset" / "processed" / "data_clean.csv"
    figures_dir = base_dir / "outputs" / "figures"

    if processed_file.exists():
        processed_file.unlink()

    if figures_dir.exists():
        for f in figures_dir.iterdir():
            if f.is_file():
                f.unlink()


def run_script(script_path: Path) -> None:
    print(f"Running {script_path.name}...")
    start = time.time()
    
    try:
        subprocess.run(
            [sys.executable, str(script_path)],
            check=True,
            capture_output=False  # Biarkan output terlihat di terminal
        )
    except subprocess.CalledProcessError:
        print(f"Failed to run {script_path.name}")
        sys.exit(1)
        
    print(f"Done in {time.time() - start:.2f}s\n")


def main():
    print("Starting Analysis Pipeline")
    clean_outputs(BASE_DIR)

    scripts = [
        "0_data_preparation.py",
        "1_analisis_deskriptif.py",
        "2_uji_hipotesis_chisquare.py",
        "3_uji_anova.py",
        "4_analisis_regresi.py"
    ]

    for script in scripts:
        run_script(NOTEBOOKS_DIR / script)

    print("Pipeline Completed Successfully.")


if __name__ == "__main__":
    main()
