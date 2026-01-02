"""
Regresi Linear Berganda: Memodelkan pengaruh faktor terhadap G3.
"""

import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.stattools import durbin_watson
from scipy.stats import jarque_bera
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent
INPUT_FILE = PROJECT_ROOT / "dataset" / "processed" / "data_clean.csv"
ALPHA = 0.05


def load_data(file_path: Path) -> pd.DataFrame:
    if not file_path.exists():
        raise FileNotFoundError(f"Clean data not found: {file_path}")
    return pd.read_csv(file_path)


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

    # 2. Multicollinearity
    vif = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
    print(f"  Max VIF: {max(vif):.2f}")

    # 3. Homoscedasticity
    _, p_homo, _, _ = het_breuschpagan(model.resid, X)
    print(f"  Homoscedasticity (Breusch-Pagan): p={p_homo:.4f}")

    # 4. Autocorrelation
    dw = durbin_watson(model.resid)
    print(f"  Autocorrelation (Durbin-Watson): {dw:.2f}")


def main():
    df = load_data(INPUT_FILE)
    
    target = "G3"
    features = ["studytime", "absences", "G1"]
    
    model, X = fit_model(df, target, features)
    print(model.summary())
    
    check_assumptions(model, X)


if __name__ == "__main__":
    main()
