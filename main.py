"""
This is a demo of the mitosheet library. It's a simple streamlit app that connects to a snowflake database and displays the results of a SQL query in a spreadsheet.
"""

import streamlit as st
import pandas as pd
from mitosheet.streamlit.v1 import spreadsheet
from queries import *
from credentials import ACCOUNT, PASSWORD, USER

st.set_page_config(layout="wide")
st.title("Explore Financial Data in Snowflake")

st.markdown("""
This app is connected to a Swnowflake database that contains financial and economic data including: central bank rates, FDIC insurnace data, bank financials, etc. 

The data is aggregated by [Cybersyn](https://docs.cybersyn.com/our-data-products/economic-and-financial/financial-and-economic-essentials?utm_source=snowflake.com&utm_medium=website&utm_campaign=website_docs) from the following sources: FDIC, FFIEC, FRED, BLS, CFPB, Bank of England, Bank of International Settlements, Bank of Canada, Banco de Mexico, and Banco Central do Brasil.

The app is already connected to the database and comes preloaded some SQL queries to pull interesting datasets, so all you need to do is select a dataset and start exploring. No coding required!
""")

# Initialize connection.
conn = st.experimental_connection(
    'snowpark', 
    account=ACCOUNT,
    user=USER,
    password=PASSWORD,
    warehouse="COMPUTE_WH",
    database="CYBERSYN_FINANCIAL__ECONOMIC_ESSENTIALS",
    schema="cybersyn",
    client_session_keep_alive = True
)

option = st.selectbox('#### What financial dataset do you want to explore?', queries_dict.keys())

st.markdown("###### Data Description")
st.write(queries_dict[option]["description"])

# Perform query.
df = conn.query(queries_dict[option]['query'], ttl=600)

# If the df has a date column, convert it to datetime
if "DATE" in df.columns:
    df["DATE"] = pd.to_datetime(df["DATE"])

spreadsheet(df)

