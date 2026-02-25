import pandas as pd


def convert_to_dataframe(items):
    records = []

    for item in items:
        row = {}
        row["Item Name"] = item["name"]

        for col in item["column_values"]:
            col_name = col["column"]["title"]
            row[col_name] = col["text"]

        records.append(row)

    df = pd.DataFrame(records)
    return df


def clean_dataframe(df):
    df.columns = df.columns.str.strip()

    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].str.replace(",", "", regex=False)
            df[col] = df[col].str.replace("₹", "", regex=False)
            df[col] = df[col].str.replace("%", "", regex=False)

    # Convert numeric-like columns
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="ignore")

    # Convert date-like columns
    for col in df.columns:
        if "date" in col.lower() or "month" in col.lower():
            df[col] = pd.to_datetime(df[col], errors="coerce")

    return df