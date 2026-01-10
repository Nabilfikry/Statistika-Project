
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
import scipy.stats as stats
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent
INPUT_FILE = PROJECT_ROOT / "dataset" / "processed" / "data_clean.csv"
FIG_DIR = PROJECT_ROOT / "outputs" / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

def load_data(file_path: Path) -> pd.DataFrame:
    return pd.read_csv(file_path)

def plot_correlation_heatmap(df, predictors, target):
    cols = predictors + [target]
    corr_matrix = df[cols].corr()

    plt.figure(figsize=(12, 10))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5, vmin=-1, vmax=1)
    plt.title("Matriks Korelasi Pearson (Predictors & Target)", fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(FIG_DIR / "4_heatmap_korelasi.png", dpi=300)
    print("Grafik Heatmap Korelasi tersimpan di outputs/figures.")
    plt.close()
    
    print("\n=== NILAI KORELASI TERHADAP G3 (TARGET) ===")
    print(corr_matrix["G3"].sort_values(ascending=False))

def plot_assumptions(model, residuals, y_pred):
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    stats.probplot(residuals, dist="norm", plot=plt)
    plt.title("Normal Q-Q Plot (Residuals)")
    
    plt.subplot(1, 2, 2)
    plt.scatter(y_pred, residuals, alpha=0.5, color='blue')
    plt.axhline(0, color='red', linestyle='--')
    plt.xlabel("Fitted Values")
    plt.ylabel("Residuals")
    plt.title("Residuals vs Fitted (Homoscedasticity)")
    
    plt.tight_layout()
    plt.savefig(FIG_DIR / "4_regresi_asumsi.png", dpi=300)
    plt.close()

def main():
    df = load_data(INPUT_FILE)
    
    predictors = [
        "age", "sex_code", "Medu", "Fedu", 
        "studytime", "failures", "absences", 
        "goout", "Dalc", "Walc", "health", 
        "freetime", "famrel", "internet_code"
    ]
    target = "G3"
    
    available_predictors = [col for col in predictors if col in df.columns]
    
    print(f"\nVariabel Independen Terpilih ({len(available_predictors)}): {available_predictors}")
    
    plot_correlation_heatmap(df, available_predictors, target)
    
    X = df[available_predictors]
    y = df[target]
    
    X = sm.add_constant(X)
    
    model = sm.OLS(y, X).fit()
    
    print("\n=== HASIL REGRESI LINEAR BERGANDA (FINAL) ===")
    print(model.summary())
    
    print("\n=== Uji Multikolinearitas (VIF) ===")
    vif_data = pd.DataFrame()
    vif_data["feature"] = X.columns
    vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(len(X.columns))]
    print(vif_data)
    
    residuals = model.resid
    y_pred = model.predict(X)
    plot_assumptions(model, residuals, y_pred)

if __name__ == "__main__":
    main()