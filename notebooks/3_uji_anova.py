import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import f_oneway
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent
INPUT_FILE = PROJECT_ROOT / "dataset" / "processed" / "data_clean.csv"
FIG_DIR = PROJECT_ROOT / "outputs" / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

ALPHA = 0.05

def plot_boxplot_anova(df):
    plt.figure(figsize=(10, 6))
    order = df.groupby("Mjob")["G3"].median().sort_values().index
    
    sns.boxplot(x="Mjob", y="G3", data=df, order=order, palette="Set2")
    sns.stripplot(x="Mjob", y="G3", data=df, order=order, color='black', alpha=0.3, jitter=True)
    
    plt.title("Distribusi Nilai G3 Berdasarkan Pekerjaan Ibu", fontsize=14)
    plt.xlabel("Pekerjaan Ibu")
    plt.ylabel("Nilai Akhir (G3)")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(FIG_DIR / "3_anova_boxplot.png", dpi=300)
    print("Grafik Boxplot ANOVA tersimpan.")
    plt.close()

def main():
    df = pd.read_csv(INPUT_FILE)
    
    print("\n=== UJI ONE-WAY ANOVA ===")
    print("H0: Rata-rata nilai G3 sama untuk semua pekerjaan ibu.")
    print("H1: Minimal ada satu pekerjaan ibu yang rata-rata nilainya berbeda.")
    
    groups = [df[df["Mjob"] == job]["G3"] for job in df["Mjob"].unique()]
    
    f_stat, p_value = f_oneway(*groups)
    
    print(f"\nF-Statistic : {f_stat:.4f}")
    print(f"P-value     : {p_value:.4f}")
    
    if p_value < ALPHA:
        print("KESIMPULAN: Tolak H0. Ada perbedaan signifikan rata-rata nilai berdasarkan pekerjaan ibu.")
        print("\n--- Melakukan Uji Lanjut (Post-Hoc: Tukey HSD) ---")
        
        tukey = pairwise_tukeyhsd(endog=df['G3'], groups=df['Mjob'], alpha=ALPHA)
        print(tukey)
        
        with open(PROJECT_ROOT / "outputs" / "tukey_results.txt", "w") as f:
            f.write(str(tukey))
            
    else:
        print("KESIMPULAN: Gagal Tolak H0. Tidak ada perbedaan rata-rata yang signifikan.")
    
    plot_boxplot_anova(df)

if __name__ == "__main__":
    main()