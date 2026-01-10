import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent
(PROJECT_ROOT / "dataset" / "processed").mkdir(parents=True, exist_ok=True)

RAW_FILE = PROJECT_ROOT / "dataset" / "raw" / "student-por.csv"
OUTPUT_FILE = PROJECT_ROOT / "dataset" / "processed" / "data_clean.csv"

def load_data(file_path: Path) -> pd.DataFrame:
    try:
        return pd.read_csv(file_path, sep=";")
    except Exception as e:
        raise ValueError(f"Gagal membaca CSV: {e}")

def clean_and_encode_data(df: pd.DataFrame) -> pd.DataFrame:
    cols = [
        "school", "sex", "age", "address", "famsize", "Pstatus", 
        "Medu", "Fedu", "Mjob", "Fjob", "guardian", 
        "traveltime", "studytime", "failures", "schoolsup", "famsup", 
        "paid", "activities", "higher", "internet", "romantic", 
        "famrel", "freetime", "goout", "Dalc", "Walc", "health", "absences", 
        "G1", "G2", "G3"
    ]
    df_clean = df[cols].copy()
    
    df_clean.dropna(inplace=True)
    df_clean = df_clean[df_clean["G3"].between(0, 20)]

    binary_cols = {
        "sex": {"F": 0, "M": 1},
        "address": {"R": 0, "U": 1},
        "famsize": {"LE3": 0, "GT3": 1},
        "Pstatus": {"A": 0, "T": 1},
        "schoolsup": {"no": 0, "yes": 1},
        "famsup": {"no": 0, "yes": 1},
        "paid": {"no": 0, "yes": 1},
        "activities": {"no": 0, "yes": 1},
        "higher": {"no": 0, "yes": 1},
        "internet": {"no": 0, "yes": 1},
        "romantic": {"no": 0, "yes": 1}
    }
    
    for col, mapping in binary_cols.items():
        df_clean[f"{col}_code"] = df_clean[col].map(mapping)

    print(f"Data cleaned. Ukuran final: {df_clean.shape}")
    return df_clean

def main():
    if not RAW_FILE.exists():
        print(f"Error: File {RAW_FILE} tidak ditemukan. Pastikan dataset ada di folder dataset/raw.")
        return

    df = load_data(RAW_FILE)
    df_final = clean_and_encode_data(df)
    
    df_final.to_csv(OUTPUT_FILE, index=False)
    print(f"Data sukses disimpan di: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()