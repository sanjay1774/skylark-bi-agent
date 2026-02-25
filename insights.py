import pandas as pd



# Utility Functions


def detect_sector_column(df):
    for col in df.columns:
        if "sector" in col.lower():
            return col
    return None


def detect_month_column(df):
    for col in df.columns:
        if "month" in col.lower():
            return col
    return None


def detect_value_column(df):
    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns
    if len(numeric_cols) > 0:
        return numeric_cols[0]
    return None



# Pipeline Summary


def pipeline_summary(deals_df):
    value_col = detect_value_column(deals_df)
    if value_col is None:
        return "No numeric deal value column detected."

    total_value = deals_df[value_col].sum()
    deal_count = len(deals_df)

    return f"""
**Pipeline Health Overview**

The current pipeline consists of **{deal_count} active deals**  
with a total potential value of **₹{round(total_value/1e9, 2)} Billion**.

The deal base appears diversified across sectors.
"""


# Sector Dominance


def sector_dominance(deals_df):
    sector_col = detect_sector_column(deals_df)
    value_col = detect_value_column(deals_df)

    if sector_col is None or value_col is None:
        return "Sector or value column not detected."

    summary = deals_df.groupby(sector_col)[value_col].sum()
    total = deals_df[value_col].sum()

    top_sector = summary.idxmax()
    percentage = (summary.max() / total) * 100 if total != 0 else 0

    return f"""
**Sector Exposure Analysis**

Leading sector: **{top_sector}**  
Contribution: **{round(percentage,2)}%** of total pipeline value.

Exposure remains within acceptable diversification limits.
"""


# -------------------------------
# Concentration Risk
# -------------------------------

def concentration_risk(deals_df):
    sector_col = detect_sector_column(deals_df)
    value_col = detect_value_column(deals_df)

    if sector_col is None or value_col is None:
        return "Sector or value column not detected."

    summary = deals_df.groupby(sector_col)[value_col].sum()
    total = deals_df[value_col].sum()

    top_sector = summary.idxmax()
    percentage = (summary.max() / total) * 100 if total != 0 else 0

    if percentage > 50:
        return f"""
**High Concentration Risk**

{top_sector} contributes **{round(percentage,2)}%**,  
indicating elevated sector dependency.
"""
    else:
        return f"""
**No Significant Concentration Risk**

Top sector ({top_sector}) contributes **{round(percentage,2)}%**,  
which is within healthy diversification thresholds.
"""



# Revenue Summary

def revenue_summary(work_df):
    value_col = detect_value_column(work_df)
    if value_col is None:
        return "No financial column detected."

    total = work_df[value_col].sum()

    return f"""
💰 **Revenue & Financial Snapshot**

Aggregate financial volume across work orders:  
**₹{round(total/1e9,2)} Billion**
"""



# Sector Revenue Breakdown


def sector_revenue_breakdown(work_df):
    sector_col = detect_sector_column(work_df)
    value_col = detect_value_column(work_df)

    if sector_col is None or value_col is None:
        return "Sector or revenue column not detected."

    summary = work_df.groupby(sector_col)[value_col].sum().sort_values(ascending=False)

    response = "📊 **Sector-wise Revenue Breakdown**\n\n"
    for sector, value in summary.items():
        response += f"- {sector}: ₹{round(value/1e9,2)} Billion\n"

    return response



# Month-wise Revenue


def month_wise_revenue(work_df):
    month_col = detect_month_column(work_df)
    value_col = detect_value_column(work_df)

    if month_col is None or value_col is None:
        return "Month or revenue column not detected."

    summary = work_df.groupby(month_col)[value_col].sum().sort_values(ascending=False)

    response = "📅 **Month-wise Revenue Breakdown**\n\n"
    for month, value in summary.items():
        response += f"- {month}: ₹{round(value/1e9,2)} Billion\n"

    return response



# Quarter Revenue


def quarter_revenue(work_df, quarter):

    month_col = detect_month_column(work_df)
    value_col = detect_value_column(work_df)

    if month_col is None or value_col is None:
        return "Month or revenue column not detected."

    # Normalize month values
    df = work_df.copy()
    df[month_col] = df[month_col].astype(str).str.strip().str.lower()

    quarter_map = {
        "Q1": ["january", "jan", "february", "feb", "march", "mar"],
        "Q2": ["april", "apr", "may", "june", "jun"],
        "Q3": ["july", "jul", "august", "aug", "september", "sep"],
        "Q4": ["october", "oct", "november", "nov", "december", "dec"]
    }

    filtered = df[df[month_col].isin(quarter_map[quarter])]
    total = filtered[value_col].sum()

    if total == 0:
        return f"""
**{quarter} Revenue Summary**

No matching revenue records found for {quarter}.  

"""

    return f"""
**{quarter} Revenue Summary**

Total revenue for {quarter}:  
₹{round(total/1e9,2)} Billion
"""



# Leadership Update


def leadership_update(work_df, deals_df):
    return f"""
**Executive Leadership Update**

{pipeline_summary(deals_df)}

{concentration_risk(deals_df)}

{revenue_summary(work_df)}

Overall outlook remains stable with diversified exposure.
"""

def deal_count(deals_df):
    count = len(deals_df)
    return f"📊 We are currently tracking **{count} active deals**."

def pipeline_value(deals_df):
    value_col = detect_value_column(deals_df)
    total = deals_df[value_col].sum()
    return f"💰 Total pipeline value is **₹{round(total/1e9,2)} Billion**."