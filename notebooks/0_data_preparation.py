"""
Membersihkan data student-por.csv agar siap dianalisis.
"""

import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent
RAW_FILE = PROJECT_ROOT / "dataset" / "raw" / "student-por.csv"
OUTPUT_DIR = PROJECT_ROOT / "dataset" / "processed"
OUTPUT_FILE = OUTPUT_DIR / "data_clean.csv"


def validate_input(file_path: Path) -> None:
    if not file_path.exists():
        raise FileNotFoundError(f"Input file not found: {file_path}")


def load_data(file_path: Path) -> pd.DataFrame:
    try:
        return pd.read_csv(file_path, sep=";")
    except Exception as e:
        raise ValueError(f"Failed to read CSV: {e}")


def validate_columns(df: pd.DataFrame, required_cols: list) -> None:
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")


def clean_data(df: pd.DataFrame, cols: list) -> pd.DataFrame:
    df_clean = df[cols].copy()
    
    # Filter valid grades (0-20)
    df_clean = df_clean[df_clean["G3"].between(0, 20)]
    
    # Remove missing values
    df_clean.dropna(inplace=True)
    
    if df_clean.empty:
        raise ValueError("Dataset is empty after cleaning")
        
    return df_clean


def main():
    validate_input(RAW_FILE)

    required_cols = [
        "G3", "sex", "Mjob", "higher", 
        "absences", "studytime", "age", "G1"
    ]

    df = load_data(RAW_FILE)
    validate_columns(df, required_cols)

    df_clean = clean_data(df, required_cols)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df_clean.to_csv(OUTPUT_FILE, index=False)
    
    print(f"Data cleaned and saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
