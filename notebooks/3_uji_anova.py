"""
One-Way ANOVA: Menguji perbedaan rata-rata nilai G3 berdasarkan pekerjaan ibu.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import f_oneway, shapiro
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent
INPUT_FILE = PROJECT_ROOT / "dataset" / "processed" / "data_clean.csv"
FIG_DIR = PROJECT_ROOT / "outputs" / "figures"
ALPHA = 0.05


def load_data(file_path: Path) -> pd.DataFrame:
    if not file_path.exists():
        raise FileNotFoundError(f"Clean data not found: {file_path}")
    return pd.read_csv(file_path)


def check_normality(df: pd.DataFrame) -> None:
    print("Normality Test (Shapiro-Wilk):")
    for group in df["Mjob"].unique():
        data = df[df["Mjob"] == group]["G3"]
        if len(data) >= 3:
            _, p = shapiro(data)
            print(f"  {group}: p={p:.4f}")


def perform_anova(df: pd.DataFrame) -> None:
    groups = [group["G3"].values for _, group in df.groupby("Mjob")]
    if len(groups) < 2:
        raise ValueError("Not enough groups for ANOVA")

    f_stat, p = f_oneway(*groups)
    print(f"ANOVA F-Stat: {f_stat:.4f}, P-Value: {p:.4f}")

    if p < ALPHA:
        print("Result: Reject H0 (Significant difference in means)")
    else:
        print("Result: Fail to reject H0 (No significant difference)")


def plot_boxplot(df: pd.DataFrame, output_path: Path) -> None:
    plt.figure(figsize=(8, 5))
    sns.boxplot(x="Mjob", y="G3", data=df, palette="Set3")
    plt.title("Distribusi G3 Berdasarkan Mjob")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def main():
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    df = load_data(INPUT_FILE)
    
    check_normality(df)
    perform_anova(df)
    plot_boxplot(df, FIG_DIR / "4_boxplot_anova.png")


if __name__ == "__main__":
    main()
