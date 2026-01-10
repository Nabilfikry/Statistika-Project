import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import chi2_contingency
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent
INPUT_FILE = PROJECT_ROOT / "dataset" / "processed" / "data_clean.csv"
FIG_DIR = PROJECT_ROOT / "outputs" / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

ALPHA = 0.05

def plot_stacked_bar(df):
    plt.figure(figsize=(8, 6))
    ct = pd.crosstab(df['sex'], df['higher'], normalize='index') * 100
    ax = ct.plot(kind='bar', stacked=True, color=['#e74c3c', '#2ecc71'], alpha=0.8)
    
    plt.title("Proporsi Keinginan Melanjutkan Studi Berdasarkan Gender", fontsize=12)
    plt.ylabel("Persentase (%)")
    plt.xlabel("Gender (F=Wanita, M=Pria)")
    plt.legend(title="Ingin Kuliah?", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(FIG_DIR / "2_chisquare_sex_higher.png", dpi=300)
    print("Grafik Chi-Square tersimpan.")
    plt.close()

def main():
    df = pd.read_csv(INPUT_FILE)
    
    print("\n=== UJI HIPOTESIS: CHI-SQUARE ===")
    print("H0: Tidak ada hubungan antara Gender dan Keinginan Kuliah (Independen)")
    print("H1: Ada hubungan antara Gender dan Keinginan Kuliah")
    
    contingency_table = pd.crosstab(df["sex"], df["higher"])
    print("\nTabel Kontingensi:")
    print(contingency_table)
    
    chi2, p, dof, expected = chi2_contingency(contingency_table)
    
    print(f"\nChi-Square Stat : {chi2:.4f}")
    print(f"P-value         : {p:.4f}")
    print(f"Alpha           : {ALPHA}")
    
    if p < ALPHA:
        print("KESIMPULAN: Tolak H0. Ada hubungan signifikan antara Gender dan Keinginan Kuliah.")
    else:
        print("KESIMPULAN: Gagal Tolak H0. Tidak cukup bukti menyatakan ada hubungan (Independen).")
    
    plot_stacked_bar(df)

if __name__ == "__main__":
    main()