from pymongo import MongoClient
import streamlit as st


@st.cache_resource
def connect_to_client():
    return MongoClient(st.secrets["mongodb"]["uri"])

@st.cache_resource
def connect_to_db():
    client = connect_to_client()
    return client['requestdb']

@st.cache_resource
def get_collection(collection_name):
    my_db = connect_to_db()
    return my_db[collection_name]