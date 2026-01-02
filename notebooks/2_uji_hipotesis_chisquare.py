"""
Uji Independensi Chi-Square: Gender vs Minat Kuliah.
"""

import pandas as pd
from scipy.stats import chi2_contingency
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent
INPUT_FILE = PROJECT_ROOT / "dataset" / "processed" / "data_clean.csv"
ALPHA = 0.05


def load_data(file_path: Path) -> pd.DataFrame:
    if not file_path.exists():
        raise FileNotFoundError(f"Clean data not found: {file_path}")
    return pd.read_csv(file_path)


def perform_test(df: pd.DataFrame) -> None:
    if "sex" not in df.columns or "higher" not in df.columns:
        raise ValueError("Missing required columns: sex, higher")

    contingency = pd.crosstab(df["sex"], df["higher"])
    chi2, p, dof, _ = chi2_contingency(contingency)

    print(f"Chi-Square Statistic: {chi2:.4f}")
    print(f"P-Value: {p:.4f}")

    if p < ALPHA:
        print("Result: Reject H0 (Significant relationship)")
    else:
        print("Result: Fail to reject H0 (No significant relationship)")


def main():
    df = load_data(INPUT_FILE)
    perform_test(df)


if __name__ == "__main__":
    main()
