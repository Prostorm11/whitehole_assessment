from __future__ import annotations

import pandas as pd


REQUIRED_COLUMNS = {"pubDate", "link", "content", "source_id"}


def read_input_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    return df


def write_output_csv(df: pd.DataFrame, path: str) -> None:
    df.to_csv(path, index=False)