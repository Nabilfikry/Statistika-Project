import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent
INPUT_FILE = PROJECT_ROOT / "dataset" / "processed" / "data_clean.csv"
FIG_DIR = PROJECT_ROOT / "outputs" / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

def load_data(file_path: Path) -> pd.DataFrame:
    return pd.read_csv(file_path)

def plot_histogram_g3(df):
    plt.figure(figsize=(8, 5))
    sns.histplot(df["G3"], kde=True, color="#2c3e50", bins=15, alpha=0.6)
    plt.axvline(df["G3"].mean(), color="red", linestyle="--", label=f"Mean: {df['G3'].mean():.2f}")
    plt.title("Distribusi Nilai Akhir Siswa (G3)", fontsize=14, fontweight='bold')
    plt.xlabel("Nilai Akhir (0-20)")
    plt.ylabel("Frekuensi")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIG_DIR / "1_distribusi_G3.png", dpi=300)
    plt.close()

def plot_demographics(df):
    plt.figure(figsize=(6, 6))
    df["sex"].value_counts().plot.pie(autopct="%1.1f%%", startangle=90, colors=['#ff9999','#66b3ff'])
    plt.title("Proporsi Jenis Kelamin Siswa", fontweight='bold')
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "1_pie_sex.png", dpi=300)
    plt.close()

    plt.figure(figsize=(8, 5))
    sns.countplot(y="Mjob", data=df, order=df["Mjob"].value_counts().index, palette="viridis")
    plt.title("Distribusi Pekerjaan Ibu", fontweight='bold')
    plt.xlabel("Jumlah")
    plt.ylabel("Pekerjaan")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "1_bar_Mjob.png", dpi=300)
    plt.close()

def main():
    df = load_data(INPUT_FILE)
    print("Membuat Visualisasi Deskriptif...")
    plot_histogram_g3(df)
    plot_demographics(df)
    print(f"Selesai. Gambar tersimpan di {FIG_DIR}")

if __name__ == "__main__":
    main()