import pandas as pd
import streamlit as st


@st.cache_data
def load_dataframe(df):
    # return pd.DataFrame(columns=["requestor", "client", "agency", "request_date", "team", "request_type", "details", "url"])
    return df


def add_row(new_row):
    df = load_dataframe()
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    st.dataframe(df)
    return df

@st.cache_data
def load_or_update(df=None):
    if df is None:
        return pd.DataFrame(columns=["A", "B", "C"])
    else:
        return df