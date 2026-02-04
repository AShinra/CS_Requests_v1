from pymongo import MongoClient
import streamlit as st
import time


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


def check_email_exists(user_email):
    users_collection = get_collection('users')
    result = users_collection.find_one({'email':user_email})
    if result:
        return True

def create_user(userdata):
    with st.spinner("Creating user in database..."):
        
        users_collection = get_collection('users')
        users_collection.insert_one({
            'name':userdata['name'],
            'username':userdata['username'],
            'email':userdata['email'],
            'password_hash':userdata['password'],  # In production, hash the password
            'rights':'user'})

        time.sleep(10)
        st.rerun()