import sqlite3
import pandas as pd


def create_database(csv_path, db_path='data/covid.db'):
    df = pd.read_csv(csv_path, parse_dates=['date'])

    mask = df['continent'].isna()
    df = df[~mask].reset_index(drop=True)

    conn = sqlite3.connect(db_path)
    df.to_sql('covid', conn, if_exists='replace', index=False)
    conn.close()

    print(f"Database created at {db_path}")
    print(f"Rows loaded: {len(df)}")


def query(db_path, sql):
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(sql, conn)
    conn.close()
    return df