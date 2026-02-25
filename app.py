import streamlit as st
import matplotlib.pyplot as plt

from monday_client import fetch_board_data
from data_processor import convert_to_dataframe, clean_dataframe
from insights import *

st.set_page_config(page_title="Monday BI Agent", layout="wide")
st.title("🚀 Monday Business Intelligence Agent")

WORK_BOARD = st.secrets["WORK_ORDER_BOARD_ID"]
DEAL_BOARD = st.secrets["DEAL_BOARD_ID"]

@st.cache_data
def load_data():
    work_items = fetch_board_data(WORK_BOARD)
    deal_items = fetch_board_data(DEAL_BOARD)

    work_df = clean_dataframe(convert_to_dataframe(work_items))
    deal_df = clean_dataframe(convert_to_dataframe(deal_items))

    return work_df, deal_df


with st.spinner("Loading data from Monday.com..."):
    work_df, deal_df = load_data()

st.success("Data Loaded Successfully")


# Sector Chart


def show_sector_chart(deal_df):
    sector_col = detect_sector_column(deal_df)
    value_col = detect_value_column(deal_df)

    if sector_col and value_col:
        summary = deal_df.groupby(sector_col)[value_col].sum().sort_values(ascending=False)

        fig, ax = plt.subplots()
        summary.plot(kind="bar", ax=ax)
        ax.set_title("Sector-wise Pipeline Distribution")
        ax.set_ylabel("Pipeline Value")
        st.pyplot(fig)



# Chat Memory


if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_query = st.chat_input("Ask about pipeline, sector exposure, revenue, month, quarter, or leadership update...")

if user_query:

    with st.chat_message("user"):
        st.write(user_query)

    st.session_state.messages.append({"role": "user", "content": user_query})

    query = user_query.lower()

    # ---------------- NLP Routing ----------------

    if "sector" in query and "revenue" in query:
        response = sector_revenue_breakdown(work_df)

    elif "month" in query:
        response = month_wise_revenue(work_df)

    elif "q1" in query:
        response = quarter_revenue(work_df, "Q1")

    elif "q2" in query:
        response = quarter_revenue(work_df, "Q2")

    elif "q3" in query:
        response = quarter_revenue(work_df, "Q3")

    elif "q4" in query or "this quarter" in query:
        response = quarter_revenue(work_df, "Q4")

    elif any(word in query for word in ["diversified", "exposure", "breakdown"]):
        response = sector_dominance(deal_df)
        show_sector_chart(deal_df)

    elif any(word in query for word in ["dominates", "top sector"]):
        response = sector_dominance(deal_df)
        show_sector_chart(deal_df)

    elif any(word in query for word in ["risk", "concentration", "dependency"]):
        response = concentration_risk(deal_df)

    elif any(word in query for word in ["pipeline", "deal", "opportunity"]):
        response = pipeline_summary(deal_df)

    elif any(word in query for word in ["revenue", "financial", "billing"]):
        response = revenue_summary(work_df)

    elif any(word in query for word in ["leadership", "update", "snapshot", "board"]):
        response = leadership_update(work_df, deal_df)
    
    elif "how many" in query and "deal" in query:
        response = deal_count(deal_df)

    elif "total size" in query or "total value" in query:
        response = pipeline_value(deal_df)

    elif "pipeline" in query:
        response = pipeline_summary(deal_df)

    else:
        response = "Please ask about pipeline, sector exposure, revenue breakdown, month, quarter, or leadership update."

    with st.chat_message("assistant"):
        st.write(response)

    st.session_state.messages.append({"role": "assistant", "content": response})