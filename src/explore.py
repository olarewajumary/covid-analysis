import pandas as pd

def load_data(path):
    df = pd.read_csv(path, parse_dates=['date'])
    return df

def basic_info(df):
    print(f"Shape: {df.shape}")
    print(f"\nDate range: {df['date'].min()} to {df['date'].max()}")
    print(f"\nCountries: {df['location'].nunique()}")
    print(f"\nContinents: {df['continent'].dropna().unique().tolist()}")
    print(f"\nMissing values:\n{df.isnull().sum()[df.isnull().sum() > 0]}")

def clean_locations(df):
    mask = df['continent'].isna()
    df = df[~mask].reset_index(drop=True)
    return df