"""
Melakukan analisis statistik deskriptif dan visualisasi dasar.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent
INPUT_FILE = PROJECT_ROOT / "dataset" / "processed" / "data_clean.csv"
FIG_DIR = PROJECT_ROOT / "outputs" / "figures"


def load_data(file_path: Path) -> pd.DataFrame:
    if not file_path.exists():
        raise FileNotFoundError(f"Clean data not found: {file_path}")
    return pd.read_csv(file_path)


def plot_histogram(df: pd.DataFrame, output_path: Path) -> None:
    plt.figure(figsize=(8, 5))
    sns.histplot(df["G3"], kde=True, color="skyblue", bins=15)
    plt.axvline(df["G3"].mean(), color="red", linestyle="--")
    plt.title("Distribusi Nilai Akhir (G3)")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def plot_pie_chart(df: pd.DataFrame, col: str, output_path: Path) -> None:
    plt.figure(figsize=(6, 6))
    df[col].value_counts().plot.pie(autopct="%1.1f%%", startangle=90)
    plt.title(f"Proporsi {col}")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def plot_bar_chart(df: pd.DataFrame, col: str, output_path: Path) -> None:
    plt.figure(figsize=(8, 5))
    counts = df[col].value_counts()
    sns.barplot(x=counts.index, y=counts.values, palette="viridis")
    plt.title(f"Distribusi {col}")
    plt.title(f"Distribusi {col}")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def main():
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    df = load_data(INPUT_FILE)

    # Statistics
    print(df[["G3", "absences", "studytime", "age"]].describe().round(2))

    # Visualizations
    plot_histogram(df, FIG_DIR / "1_histogram_G3.png")
    plot_pie_chart(df, "sex", FIG_DIR / "2_piechart_gender.png")
    plot_bar_chart(df, "Mjob", FIG_DIR / "3_barchart_Mjob.png")

    print(f"Figures saved to {FIG_DIR}")


if __name__ == "__main__":
    main()
