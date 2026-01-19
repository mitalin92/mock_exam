import pandas as pd


def load_data(df: pd.DataFrame) -> pd.DataFrame:
    df = pd.read_csv(df)
    return df


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    if "volume" in df.columns:
        df["volume"] = df["volume"].fillna(0)

    price_cols = ["open", "high", "low", "close"]
    for col in price_cols:
        df = df.dropna(subset=price_cols)

    return df


def safe_type_conversion(df: pd.DataFrame) -> pd.DataFrame:
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    price_cols = ["open", "high", "low", "close"]

    for col in price_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


def valid_data(df: pd.DataFrame) -> pd.DataFrame:
    invalid_rows = df["high"] < df["low"]

    df = df[~invalid_rows]

    return df


def summarize_stocks(df: pd.DataFrame) -> None:
    summary = (
        df.groupby("symbol")["close"]
        .agg(avg_close="mean", volatility="std")
        .reset_index()
    )
    summary_sorted = summary.sort_values("volatility", ascending=False)
    most_volatile_symbol = summary_sorted.iloc[0]["symbol"]
    print(f"most volatile symbol is {most_volatile_symbol}")


if __name__ == "__main__":
    df = load_data("data/stocks.csv")
    print(df.head())

    df = (
        df.pipe(handle_missing_values)
        .pipe(safe_type_conversion)
        .pipe(valid_data)
        .pipe(summarize_stocks)
    )
