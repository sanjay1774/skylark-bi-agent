import requests
import streamlit as st

API_URL = "https://api.monday.com/v2"

def run_query(query):
    headers = {
        "Authorization": st.secrets["MONDAY_API_TOKEN"],
        "Content-Type": "application/json"
    }

    response = requests.post(API_URL, json={"query": query}, headers=headers)

    if response.status_code != 200:
        raise Exception(f"API Error: {response.status_code} - {response.text}")

    return response.json()


def fetch_board_data(board_id):
    query = f"""
    query {{
      boards(ids: {board_id}) {{
        items_page(limit: 500) {{
          items {{
            name
            column_values {{
              column {{
                title
              }}
              text
            }}
          }}
        }}
      }}
    }}
    """

    result = run_query(query)

    items = result["data"]["boards"][0]["items_page"]["items"]
    return items