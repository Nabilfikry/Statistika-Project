"""
Analisis Korelasi dan Regresi Linear Berganda.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.stattools import durbin_watson
from scipy.stats import jarque_bera
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


def print_correlation(df: pd.DataFrame, cols: list) -> None:
    corr_matrix = df[cols].corr().round(3)
    print("Correlation Matrix:")
    print(corr_matrix)


def plot_correlation_heatmap(df: pd.DataFrame, cols: list, output_path: Path) -> None:
    corr_matrix = df[cols].corr()
    plt.figure(figsize=(8, 6))
    sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", center=0)
    plt.title("Correlation Heatmap")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def fit_model(df: pd.DataFrame, target: str, features: list):
    X = sm.add_constant(df[features])
    y = df[target]
    model = sm.OLS(y, X).fit()
    return model, X


def check_assumptions(model, X) -> None:
    print("\nAssumption Checks:")

    # 1. Normality
    _, p_norm = jarque_bera(model.resid)
    print(f"  Normality (Jarque-Bera): p={p_norm:.4f}")

    # 2. Multicollinearity (exclude const for interpretation)
    vif_data = pd.DataFrame({
        "Variable": X.columns,
        "VIF": [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
    })
    print("  VIF:")
    print(vif_data.to_string(index=False))

    # 3. Homoscedasticity
    _, p_homo, _, _ = het_breuschpagan(model.resid, X)
    print(f"  Homoscedasticity (Breusch-Pagan): p={p_homo:.4f}")

    # 4. Autocorrelation
    dw = durbin_watson(model.resid)
    print(f"  Autocorrelation (Durbin-Watson): {dw:.2f}")


def main():
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    df = load_data(INPUT_FILE)

    target = "G3"
    features = ["studytime", "absences", "G1"]
    all_numeric = [target] + features + ["age"]

    # Correlation Analysis
    print_correlation(df, all_numeric)
    plot_correlation_heatmap(df, all_numeric, FIG_DIR / "5_correlation_heatmap.png")

    # Regression
    print("\nRegression Model:")
    model, X = fit_model(df, target, features)
    print(model.summary())

    check_assumptions(model, X)


if __name__ == "__main__":
    main()
